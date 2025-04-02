import pickle

PRIMEFILE = 'primes.pkl'
UPPERLIMIT = 1_000_000

# This script finds Goldbach pairs for odd numbers starting from the last prime found.
# It uses a brute-force method to find the pairs.
# It also serializes the primes found to a file for future use.
# The script will continue from the last prime found in the file.
# It will also handle exceptions and save the state of the primes to a file.
# The script will run indefinitely until interrupted.
# The script will print the Goldbach pairs found for every 1000 odd numbers.

class GoldbachWorkspace:
    def __init__(self):
        self.primes = [1, 2, 3]

    def is_prime(self, n):
        for i in range(2, n):
            if n % i == 0:
                return False
        return True

    def next_prime(self):
        n = self.primes[-1] + 1
        while not self.is_prime(n):
            n += 1
        self.primes.append(n)
        # print(f"Found prime: {n}")
        return n

    def is_even(self, n):
        return n % 2 == 0

    def is_odd(self, n):
        return n % 2 != 0

    def fill_primes(self, n):
        while self.primes[-1] < n:
            self.next_prime()

    def goldbach(self, n):
        assert self.is_even(n)
        self.fill_primes(n)
        for i in range(len(self.primes)):
            for j in range(i, len(self.primes)):
                if self.primes[i] + self.primes[j] == n:
                    return [self.primes[i], self.primes[j]]
        return None

    def deserialize_primes(self):
        try:
            with open(PRIMEFILE, 'rb') as f:
                self.primes = pickle.load(f)
        except FileNotFoundError:
            print("No primes file found, starting fresh.")
            self.primes = [1, 2, 3]
        except (ValueError, pickle.UnpicklingError):
            print("Error reading primes file, starting fresh.")
            self.primes = [1, 2, 3]

    def serialize_primes(self):
        with open(PRIMEFILE, 'wb') as f:
            pickle.dump(self.primes, f)

    def run(self, upper_limit=UPPERLIMIT):
        self.deserialize_primes()
        for i in range(self.primes[-1] + 1, upper_limit, 2):
            result = self.goldbach(i)
            if result:
                if i % 1000 == 0:
                    print(f"{i} = {result[0]} + {result[1]}")
            else:
                print(f"No Goldbach pair found for {i}")
                exit(1)


if __name__ == '__main__':
    workspace = GoldbachWorkspace()
    try:
        workspace.run()
    except KeyboardInterrupt:
        print("\rProgram interrupted. Saving primes...")
        workspace.serialize_primes()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    finally:
        print("Exiting the program.")
