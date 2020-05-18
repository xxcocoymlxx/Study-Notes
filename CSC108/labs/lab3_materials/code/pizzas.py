def total_slices(num_pizzas, slices_per_pizza):
    ''' (int, int) -> int
    Return the total number of slices in num_pizzas pizzas
    that each have slices_per_pizza slices.
    >>> total_slices(2, 30)
    60
    >>> total_slices(1, 8)
    8
    '''
    return num_pizzas * slices_per_pizza


# we order 2 medium pizzas and 1 party pizza
medium_slices = total_slices(2, 8)

pieces_per_partysize = 30
party_slices = total_slices(1, pieces_per_partysize)

grand_total = medium_slices + party_slices

print("With 2 mediums and 1 partysize, we will have", grand_total, "slices")
