import argparse
from controllers.Solver import Solver


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--knowledge_base_path", help="Path to text file containing the knowledge base", required=True)
    parser.add_argument("--query_path", help="Path to text file containing queries", default=None)
    args = parser.parse_args()

    # Read knowledge base
    kb_file = open(args.knowledge_base_path)
    kb = kb_file.read()
    kb_file.close()

    # Initialize solver
    solver = Solver(knowledge_base=kb)

    # Process queries
    if args.query_path is not None:
        query_file = open(args.query_path)
        for query in query_file.readlines():
            print(solver.solve(query))
    else:
        while True:
            query = input("> ")
            print(solver.solve(query))


if __name__ == "__main__":
    main()
