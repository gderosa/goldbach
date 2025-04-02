import pickle

PRIMEFILE = 'primes.pkl'  # Default prime file
UPPERLIMIT = 1_000_000  # Default upper limit

class Goldbach:
    def __init__(self, primefile=PRIMEFILE, upper_limit=UPPERLIMIT):
        self.primefile = primefile
        self.upper_limit = upper_limit
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
            with open(self.primefile, 'rb') as f:
                self.primes = pickle.load(f)
        except FileNotFoundError:
            print("No primes file found, starting fresh.")
            self.primes = [1, 2, 3]
        except (ValueError, pickle.UnpicklingError):
            print("Error reading primes file, starting fresh.")
            self.primes = [1, 2, 3]

    def serialize_primes(self):
        with open(self.primefile, 'wb') as f:
            pickle.dump(self.primes, f)

    def run(self):
        self.deserialize_primes()
        for i in range(self.primes[-1] + 1, self.upper_limit, 2):
            result = self.goldbach(i)
            if result:
                if i % 1000 == 0:
                    print(f"{i} = {result[0]} + {result[1]}")
            else:
                print(f"No Goldbach pair found for {i}")
                exit(1)


if __name__ == '__main__':
    goldbach = Goldbach(primefile=PRIMEFILE, upper_limit=UPPERLIMIT)
    try:
        goldbach.run()
    except KeyboardInterrupt:
        print("\rProgram interrupted. Saving primes...")
        goldbach.serialize_primes()
        print(f"Primes saved in {goldbach.primefile}.")
