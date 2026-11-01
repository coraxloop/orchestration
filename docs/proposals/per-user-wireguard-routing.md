# Per-account WireGuard routing on root-full servers · `proposal:wireguard:per-account-wireguard-routing`

Status: DRAFT — initial model for owner review. Open questions at the end.

## Purpose · `sec:wireguard:purpose`

The estate's only VPN record to date is the shared instance's userspace proxy: no NET_ADMIN and no TUN device meant one wireproxy process and opt-in proxying, with everything else egressing direct. A root-full server removes that ceiling: kernel WireGuard interfaces, policy routing, and firewall marks are all available. That allows the account model's central property — every act attributable to exactly one account — to extend to network egress: each account gets its own WireGuard tunnel to the internet, and the machine routes each account's traffic into its own tunnel. One account's exit address, provider allocation, and traffic history are then that account's alone: a leaked identity or a noisy workload implicates one tunnel, revocation is one peer removal, and per-account bandwidth or destination questions have per-account answers.

## The model · `sec:wireguard:the-model`

### One tunnel per account, owned by `owner` · `sec:wireguard:one-tunnel-per-account-owned-by-owner`

Each tunneled account gets a dedicated WireGuard interface (`wg-<account>`) with its own keypair and its own provider allocation. The `owner` account creates, holds, and manages all of them — configs root-only under `/etc/wireguard/`, brought up as `wg-quick@wg-<account>` systemd units with `Table = off`, so bringing a tunnel up never rewrites the main routing table. The accounts themselves hold no tunnel keys and cannot manage interfaces; a confined `staff` account has no business with NET_ADMIN, and the whole point is that routing is imposed by the machine owner, not elected by the account.

### Routing by uid, imposed by policy rules · `sec:wireguard:routing-by-uid-imposed-by-policy-rules`

For this fictional example, `loop-a`, `loop-b`, and `loop-c` use UIDs 41001, 41002, and 41003, routing tables 101, 102, and 103, and tunnels `wg-loop-a`, `wg-loop-b`, and `wg-loop-c`, respectively. Each tunnel gets a routing table whose default route is its WireGuard interface, and a uid-range rule maps the account onto that table:

```
ip rule add uidrange 41001-41001 lookup 101   # loop-a -> table 101
ip route add default dev wg-loop-a table 101
```

The rules are installed by `owner` (via the wg-quick unit's PostUp or a small owner-managed unit), survive tunnel restarts, and are invisible to the account: processes just find their packets leaving through their tunnel. Loopback and LAN-internal traffic (the hub, SSH from the estate) stay on the main table via higher-priority rules, so per-account tunneling never breaks intra-estate operations.

### Fail-closed by default · `sec:wireguard:fail-closed-by-default`

A tunnel that is down must not silently fail over to direct egress — that would turn an outage into an identity leak. An nftables rule per tunneled account drops forward/output traffic from that uid unless it leaves through its own interface (LAN and loopback excepted). The default posture for loop accounts is therefore fail-closed: no tunnel, no internet. Whether the showcase account shares that posture is an open question below; `owner` and `administrator` deliberately stay on direct egress so machine maintenance never depends on a VPN being healthy.

### Port-forwarding · `sec:wireguard:port-forwarding`

Two distinct kinds, recorded separately:

1. **Provider-side (through the tunnel).** Inbound reachability for public services — `loop-b` or `loop-c` that must accept connections from the internet — is a forwarded port on that account's provider allocation, arriving through that account's tunnel only. The port belongs to the account's tunnel, so the public endpoint and the serving account stay aligned.
2. **Router-side (LAN).** Ports forwarded by the site router to the server's LAN address, for services that should be reachable without the VPN path. These bypass every tunnel and are estate-visible surface; each one is a deliberate, registry-recorded exception rather than a convenience.

The authoritative inventory — service, account, tunnel or router path, external port, internal port — lives in the server registry row, and a forwarded port with no registry line is a finding.

### Key and token custody · `sec:wireguard:key-and-token-custody`

All WireGuard keys for a root-full server are minted by `owner` on that server and never leave it — nothing is generated on another machine and shipped in. `owner` registers its own public keys with the VPN provider through the provider's API, acting for itself rather than being provisioned from outside, which requires the provider API token to live on the server in root-only custody. That is a deliberate extension of the original token rule: the rule's ground was an untrusted, ephemeral shared instance, and it stands unchanged there; a root-full machine owned by our own agent account is the trust domain the token protects, so holding the token is consistent with its purpose. Tunnel configs and keys never enter a git repository; the registry records the model and the inventory, not the material.

### Site access: the public endpoint comes from the provider · `sec:wireguard:site-access-the-public-endpoint-comes-from-the-provider`

Reaching the servers from outside the LAN needs a stable public address, and the provider's port-forwarding API supplies one without touching the site router: `owner` keeps an uplink tunnel to the provider and requests a forwarded public port on its allocation, which arrives through that tunnel and is pointed at the server's own inbound WireGuard listener. Roaming clients connect to the provider endpoint from anywhere; dynamic-DNS machinery and router port-forwards are both unnecessary, the site's own public IP stays out of every client config, and the endpoint survives router and ISP changes. Router-side LAN forwards remain available as deliberate registry-recorded exceptions but are not the primary path.

## Open questions for the owner · `sec:wireguard:open-questions-for-the-owner`

1. **Which accounts get tunnels?** All loop accounts plus the showcase, loops only, or a per-account decision? (`owner`/`administrator` staying direct is assumed for maintainability.)
2. **Fail posture for the showcase account** — fail-closed like the loops, or fail-open since it is a presentation seat where a dead tunnel should degrade to direct rather than to a blank screen?
3. **Provider allocation budget** — each tunneled account consumes an allocation from the provider subscription. The available budget must cover the selected accounts across the deployment, including capacity reserved for maintenance and growth; is one shared subscription the intent, or per-server subscriptions?
4. **The port-forward inventory** — which services need provider-side inbound ports today (`loop-b`? `loop-c`? anything on the showcase?), and are any router-side LAN forwards wanted at all?
5. **Rollout order** — one pilot server first, followed by the remaining servers after the model settles, or a coordinated rollout?
