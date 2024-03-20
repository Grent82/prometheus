
import asyncio
import hashlib

class AsyncCache:
    def __init__(self):
        self.cache = {}
        self.lock = asyncio.Lock()

    async def add_item(self, key, value):
        """Add an item to the cache."""
        async with self.lock:
            self.cache[key] = value

    async def update_item(self, key, value):
        """Update an existing item in the cache."""
        async with self.lock:
            if key in self.cache:
                self.cache[key] = value
            else:
                print(f"Key '{key}' does not exist in the cache. Cannot update.")

    async def get_item(self, key):
        """Retrieve an item from the cache."""
        return self.cache.get(key, None)

    async def remove_item(self, key):
        """Remove an item from the cache."""
        async with self.lock:
            if key in self.cache:
                del self.cache[key]
            else:
                print(f"Key '{key}' does not exist in the cache. Cannot remove.")

    async def clear_cache(self):
        """Clear the entire cache."""
        async with self.lock:
            self.cache.clear()

    async def display_cache(self):
        """Display the current contents of the cache."""
        async with self.lock:
            print("Current Cache Contents:")
            for key, value in self.cache.items():
                print(f"{key}: {value}")
    
    def _generate_key(self, key_string):
        """Generate a hash key from a string."""
        return hashlib.sha256(key_string.encode()).hexdigest()
