class Person: #Node

    def __init__(self, name, next = None):
        self.name = name
        self.next = next

class PeopleChain: #Linked list
    """A chain of people.

    === Attributes ===
    leader: Person | None
        The first person in the chain, or None if the chain is empty.
    """
    def __init__(self: 'PeopleChain', names: 'list of str') -> None:
        """Create people linked together in the order provided in <names>.

        The leader of the chain is the first person in <names>.
        """
        if len(names) == 0:#base case
            # No leader, representing an empty chain!
            self.leader = None
        else:
            # Set leader
            self.leader = Person(names[0])
            current_person = self.leader
            for name in names[1:]:
                # Set the link for the current person
                current_person.next = Person(name)
                # Update the current person
                # Note that current_person always refers to
                # the LAST person in the chain
                current_person = current_person.next

    # TODO: Implement the following four methods!
    def get_leader(self: 'PeopleChain') -> str:
        """Return the name of the leader of the chain.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_leader()
        'Iron Man'
        """
        return self.leader.name

    def get_second(self: 'PeopleChain') -> str:
        """Return the name of the second person in the chain.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_second()
        'Janna'
        """

        return self.leader.next.name

    def get_third(self: 'PeopleChain') -> str:
        """Return the name of the third person in the chain.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_third()
        'Kevan'
        """
        
        return self.leader.next.next.name

    def get_nth(self: 'PeopleChain', n: int) -> str:
        """Return the name of the n-th person in the chain.

        Precondition: n >= 0

        Raise ShortChainError if chain doesn't have n people.

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_nth(0)
        'Iron Man'

        >>> chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        >>> chain.get_nth(2)
        'Kevan'
        """

        curr = self.leader
        curr_index = 0

        # Iterate to (index)-th node
        while curr is not None and curr_index < n:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise ShortChainError
        else:
            return curr.name


class ShortChainError(Exception):
    pass

import doctest
doctest.testmod()
