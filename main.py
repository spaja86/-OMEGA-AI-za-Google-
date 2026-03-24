"""
OMEGA AI za Google — ulazna točka.

Korištenje:
    python main.py                     # interaktivni mod
    python main.py --query "AI 2025"   # jednostruki upit
    python main.py --evolve            # pokreni evolucijski ciklus
    python main.py --stats             # prikaži statistiku
    python main.py --reset             # resetuj evolucijsku memoriju
"""

from __future__ import annotations

import argparse
import sys


def _print_banner() -> None:
    print(
        "\n"
        "  ╔══════════════════════════════════════════════╗\n"
        "  ║          ♾️  OMEGA AI za Google  ♾️           ║\n"
        "  ║   Evolvira Google pretragu ka beskonačnosti  ║\n"
        "  ╚══════════════════════════════════════════════╝\n"
    )


def _print_results(results: list, verbose: bool = False) -> None:
    from omega_ai.result_ranker import SearchResult

    if not results:
        print("  ⚠️  Nema rezultata.")
        return
    for r in results:
        print(f"\n  [{r.rank}] {r.title}")
        print(f"       🔗 {r.url}")
        print(f"       📊 Relevantnost: {r.relevance_score:.4f}")
        if verbose and r.ai_summary:
            print(f"       🧠 AI sažetak: {r.ai_summary}")
        if verbose and r.keywords:
            print(f"       🏷️  Ključne riječi: {', '.join(r.keywords)}")


def _interactive_mode(omega) -> None:  # type: ignore[no-untyped-def]
    print("  💬 Interaktivni mod — upišite upit ili 'exit' za izlaz.\n")
    while True:
        try:
            query = input("  🔍 Upit: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  👋 Doviđenja!")
            break
        if not query:
            continue
        if query.lower() in {"exit", "quit", "izlaz"}:
            print("  👋 Doviđenja!")
            break
        if query.lower() == "stats":
            stats = omega.evolution.get_stats()
            print(f"\n  📈 Statistika: {stats}\n")
            continue
        if query.lower() == "evolve":
            strategy = omega.evolution.run_cycle()
            print(f"\n  🧬 Nova generacija: {strategy.strategy_id}\n")
            continue

        results = omega.search(query)
        _print_results(results, verbose=True)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OMEGA AI za Google — evolucijska AI pretraga"
    )
    parser.add_argument("--query", "-q", help="Upit za pretragu")
    parser.add_argument("--evolve", action="store_true", help="Pokreni evolucijski ciklus")
    parser.add_argument("--stats", action="store_true", help="Prikaži statistiku evolucije")
    parser.add_argument("--reset", action="store_true", help="Resetuj evolucijsku memoriju")
    parser.add_argument("--verbose", "-v", action="store_true", help="Detaljan ispis")
    args = parser.parse_args()

    _print_banner()

    # Kasna inicijalizacija da ne bi usporavali --help
    from omega_ai import OmegaAI

    omega = OmegaAI()

    if args.reset:
        omega.evolution.reset()
        print("  ♻️  Evolucijska memorija resetovana.\n")
        return

    if args.stats:
        stats = omega.evolution.get_stats()
        print("  📈 OMEGA AI Statistika Evolucije")
        print("  " + "─" * 40)
        for key, value in stats.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")
        print()
        return

    if args.evolve:
        strategy = omega.evolution.run_cycle()
        print(f"  🧬 Evolucijski ciklus završen.")
        print(f"     Nova strategija: {strategy.strategy_id}")
        print(f"     Generacija: {omega.evolution.get_stats()['generation']}\n")
        return

    if args.query:
        print(f"  🔍 Pretraživanje: '{args.query}'\n")
        results = omega.search(args.query)
        _print_results(results, verbose=args.verbose)
        print()
        return

    # Default: interaktivni mod
    _interactive_mode(omega)


if __name__ == "__main__":
    main()
