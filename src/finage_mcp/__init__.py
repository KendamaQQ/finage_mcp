from . import server
import asyncio

def main():
    server.run()

if __name__ == "__main__":
    main()

__all__ = ["main", "server"]