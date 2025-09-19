import dns.message
import dns.query
import dns.rdatatype
import random

ROOT_SERVERS = [
    "198.41.0.4", "199.9.14.201", "192.33.4.12", "199.7.91.13",
    "192.203.230.10", "192.5.5.241", "192.112.36.4", "198.97.190.53",
    "192.36.148.17", "192.58.128.30", "193.0.14.129", "199.7.83.42",
    "202.12.27.33"
]

MAX_HOPS = 10


def short_list(items, max_show=3):
    """Truncate long lists for readability."""
    if len(items) > max_show:
        return items[:max_show] + [f"… ({len(items)-max_show} more)"]
    return items


def resolve(name, rtype="A", depth=0, root=True):
    """
    Iterative resolver with compact, labeled logging.
    """
    indent = "  " * depth
    print(f"\n{indent}[scenario] Resolving {name} ({rtype})")

    servers = ROOT_SERVERS.copy()
    tried = set()

    for hop in range(1, MAX_HOPS + 1):
        if not servers:
            print(f"{indent}[fail] No servers left to query at hop {hop}")
            if root:  # only print summary for top-level scenario
                print(f"{indent}[done] {name} ({rtype}) →  failed (no servers left)")
            return None

        ns = random.choice(servers)
        servers.remove(ns)
        tried.add(ns)

        try:
            query = dns.message.make_query(name, rtype)
            response = dns.query.udp(query, ns, timeout=3)
        except Exception as e:
            print(f"{indent}[hop {hop}] {ns} → [error] {e}")
            continue

        # Answer section
        if response.answer:
            for rrset in response.answer:
                if rrset.rdtype == dns.rdatatype.CNAME:
                    target = rrset[0].target.to_text()
                    print(f"{indent}[hop {hop}] {ns} → [CNAME] {rrset.name} → {target}")
                    result = resolve(target, rtype, depth + 1, root=False)
                    if root:
                        if result:
                            print(f"{indent}[done] {name} ({rtype}) →  resolved via CNAME to {short_list(result)}")
                        else:
                            print(f"{indent}[done] {name} ({rtype}) →  failed (CNAME target unresolved)")
                    return result
                elif rrset.rdtype == dns.rdatatype.from_text(rtype):
                    ips = [r.to_text() for r in rrset]
                    print(f"{indent}[hop {hop}] {ns} → [ANSWER] {rrset.name} → {short_list(ips)}")
                    if root:
                        print(f"{indent}[done] {name} ({rtype}) →  resolved to {short_list(ips)}")
                    return ips

        # Referral (with glue)
        if response.additional:
            glue_ips = [r.to_text() for rr in response.additional for r in rr]
            print(f"{indent}[hop {hop}] {ns} → [referral + glue] {short_list(glue_ips)}")
            servers = glue_ips
            continue

        # Referral (authority-only)
        if response.authority:
            ns_records = [r.target.to_text() for rr in response.authority for r in rr if rr.rdtype == dns.rdatatype.NS]
            if ns_records:
                chosen_ns = ns_records[0]
                print(f"{indent}[hop {hop}] {ns} → [referral authority-only] need to resolve NS {chosen_ns}")
                # Resolve one NS hostname to IPs
                ips = resolve(chosen_ns, "A", depth + 1, root=False)
                if ips:
                    print(f"{indent}  ↳ resolved {chosen_ns} → {short_list(ips)}")
                    servers = ips
                continue

        print(f"{indent}[hop {hop}] {ns} → [warn] no useful data")

    print(f"{indent}[fail] Could not resolve {name} (gave up after {MAX_HOPS} hops)")
    if root:
        print(f"{indent}[done] {name} ({rtype}) →  failed (too many hops)")
    return None


if __name__ == "__main__":
    resolve("example.com", "A")
    resolve("www.google.com", "A")
    resolve("www.microsoft.com", "A")
    resolve("dnssec-failed.org", "A")
    resolve("ipv6.google.com", "AAAA")
    resolve("idontexist.ugm.ac.id", "A")

