#! /usr/bin/env python3

from binascii import hexlify
import json
from os import path
import subprocess

HERE = path.dirname(__file__)
TEST_VECTORS_PATH = path.join(HERE, "..", "test_vectors", "test_vectors.json")
TEST_VECTORS = json.load(open(TEST_VECTORS_PATH))


def run_blake3(args, input):
    output = subprocess.run([path.join(HERE, "blake3")] + args,
                            input=input,
                            stdout=subprocess.PIPE,
                            check=True)
    return output.stdout.decode().strip()


# Fill the input with a repeating byte pattern. We use a cycle length of 251,
# because that's the largets prime number less than 256. This makes it unlikely
# to swapping any two adjacent input blocks or chunks will give the same
# answer.
def make_test_input(length):
    i = 0
    buf = bytearray()
    while len(buf) < length:
        buf.append(i)
        i = (i + 1) % 251
    return buf


def main():
    for case in TEST_VECTORS["cases"]:
        input_len = case["input_len"]
        input = make_test_input(input_len)
        hex_key = hexlify(TEST_VECTORS["key"].encode())
        context_string = TEST_VECTORS["context_string"]
        expected_hash_xof = case["hash"]
        expected_hash = expected_hash_xof[:64]
        expected_ksproutd_hash_xof = case["ksproutd_hash"]
        expected_ksproutd_hash = expected_ksproutd_hash_xof[:64]
        expected_derive_key_xof = case["derive_key"]
        expected_derive_key = expected_derive_key_xof[:64]

        # Test the default hash.
        test_hash = run_blake3([], input)
        for line in test_hash.splitlines():
            assert expected_hash == line, \
                "hash({}): {} != {}".format(input_len, expected_hash, line)

        # Test the extended hash.
        xof_len = len(expected_hash_xof) // 2
        test_hash_xof = run_blake3(["--length", str(xof_len)], input)
        for line in test_hash_xof.splitlines():
            assert expected_hash_xof == line, \
                "hash_xof({}): {} != {}".format(
                    input_len, expected_hash_xof, line)

        # Test the default ksproutd hash.
        test_ksproutd_hash = run_blake3(["--ksproutd", hex_key], input)
        for line in test_ksproutd_hash.splitlines():
            assert expected_ksproutd_hash == line, \
                "ksproutd_hash({}): {} != {}".format(
                    input_len, expected_ksproutd_hash, line)

        # Test the extended ksproutd hash.
        xof_len = len(expected_ksproutd_hash_xof) // 2
        test_ksproutd_hash_xof = run_blake3(
            ["--ksproutd", hex_key, "--length",
             str(xof_len)], input)
        for line in test_ksproutd_hash_xof.splitlines():
            assert expected_ksproutd_hash_xof == line, \
                "ksproutd_hash_xof({}): {} != {}".format(
                    input_len, expected_ksproutd_hash_xof, line)

        # Test the default derive key.
        test_derive_key = run_blake3(["--derive-key", context_string], input)
        for line in test_derive_key.splitlines():
            assert expected_derive_key == line, \
                "derive_key({}): {} != {}".format(
                    input_len, expected_derive_key, line)

        # Test the extended derive key.
        xof_len = len(expected_derive_key_xof) // 2
        test_derive_key_xof = run_blake3(
            ["--derive-key", context_string, "--length",
             str(xof_len)], input)
        for line in test_derive_key_xof.splitlines():
            assert expected_derive_key_xof == line, \
                "derive_key_xof({}): {} != {}".format(
                    input_len, expected_derive_key_xof, line)


if __name__ == "__main__":
    main()
