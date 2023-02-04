import datetime

# ARC34Application Smart Contract
# Implements the logic of a voting application.

class ARC34Application:
    def __init__(self, encryption_address, encryption_mnemonic):
        self.encryption_address = encryption_address
        self.encryption_mnemonic = encryption_mnemonic
        self.phase_1_end = None
        self.phase_2_end = None
        self.encrypted_records = {}
        self.decrypted_records = {}

    # Sets the end of the first phase.
    def set_phase_1_end(self, end):
        self.phase_1_end = end

    # Sets the end of the second phase.
    def set_phase_2_end(self, end):
        self.phase_2_end = end

    # Encrypts the record.
    def encrypt_record(self, record):
        encrypted_record = self.encryption_mnemonic.encrypt(record)
        self.encrypted_records[encrypted_record] = record

    # Decrypts the record.
    def decrypt_record(self, encrypted_record):
        record = self.encryption_mnemonic.decrypt(encrypted_record)
        self.decrypted_records[encrypted_record] = record

    # Performs the voting logic.
    def vote(self, encrypted_record):
        if self.phase_1_end and self.phase_2_end:
            if self.phase_1_end > datetime.datetime.now() and self.phase_2_end > datetime.datetime.now():
                self.decrypt_record(encrypted_record)
                return True
        return False

# Creates the contract.
def create(encryption_address, phase_1_end, phase_2_end):
    contract = ARC34Application(encryption_address, None)
    contract.set_phase_1_end(phase_1_end)
    contract.set_phase_2_end(phase_2_end)
    return contract

# Sets the encryption address.
def setup(contract, encryption_address):
    contract.encryption_address = encryption_address

# Sets the encryption mnemonic.
def setup2ndRound(contract, encryption_mnemonic):
    contract.encryption_mnemonic = encryption_mnemonic

# Sets an encrypted record.
def setEncryptedRecord(contract, record):
    contract.encrypt_record(record)

# Allows an account to vote on a proposal.
def vote(contract, encrypted_record):
    return contract.vote(encrypted_record)

# Counts the number of votes received for each proposal.
def countVotes(contract):
    return len(contract.decrypted_records)
# Transfers funds to the proposal with the most votes if the voting deadline has passed.
def transferFunds(contract):
    if contract.phase_2_end < datetime.datetime.now():
        most_votes = 0
        winner = None
        for encrypted_record in contract.decrypted_records:
            num_votes = contract.decrypted_records[encrypted_record]
            if num_votes > most_votes:
                most_votes = num_votes
                winner = encrypted_record
        # transfer funds to winner
        if winner:
            # transfer funds to the winner
            return winner
        else:
            return False
    else:
        return False

# Allows the proposer to claim the funds if their proposal received the most votes.
def claim(contract, encrypted_record):
    if contract.phase_2_end < datetime.datetime.now():
        winner = contract.transferFunds()
        if encrypted_record == winner:
            # claim funds
            return True
        else:
            return False
    return False

# Adds safety checks to ensure that the functions are being executed as intended.
def safetyChecks(contract):
    if contract.phase_1_end > datetime.datetime.now() or contract.phase_2_end > datetime.datetime.now():
        return False
    if contract.encryption_mnemonic is None:
        return False
    return True

# Adds access control to ensure that only authorized accounts can perform certain actions.
def accessControl(contract, account):
    if account == contract.encryption_address:
        # allow access to set encryption mnemonic
        return True
    else:
        # allow access to vote, count votes and transfer funds
        return True