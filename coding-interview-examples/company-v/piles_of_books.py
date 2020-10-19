'''
Coding interview examples

Piles of Books

Someone gave you a large and unstable pile of books of size `starting_height`
and you want to split them into shorter piles because they'll fall over
if the piles are taller than a `stable_height`.

When you split a pile of books, you will split it into `number_of_partitions`
even piles whenever possible. So the height of the resulting piles should differ
by 1 book at most. You don't have to count piles of books that are empty. For
example, if the `starting_height` is 6 books high and `stable_height` is 5
but your `number_of_partitions` is 7 then you'd split it into 6 piles of 1 book
and one pile with zero books, which you wouldn't count.

Stop splitting when all the piles as short as `stable_height` or shorter. The
final result is the number of piles after splitting.

The only line of input contains three integers:
`starting_height`, `stable_height`, `number_of_partitions`

Example 1:
Input
13 3 2
Output
5

Explanation - Pile Iterations:
13 (`starting_height` greater than `stable_height`, so attempt to split into 2 piles)
7 6 (Both new piles exceed the `stable_height`, so split each of them.)
4 3 3 3 (Only the first pile exceeds the `stable_height`, so split it)
2 2 3 3 3 (At this point no pile exceed the `stable_height`,)

Example 2:
Input
3 2 5
Output
3

Explenation - Pile Iterations
3 (`starting_height` greater than `stable_height`, so attempt to split into 2 piles.)
1 1 1 0 0 (No pile eceed stable height, but don't count the empty piles)


'''
def split_pile(original_pile_height, number_of_partitions):
    '''
    Splits a pile into a number_of_partitions piles and evenly fills them
    '''
    new_piles = []
    for partition_number in range(0, number_of_partitions):
        new_pile_size = original_pile_height // number_of_partitions
        if original_pile_height % number_of_partitions > partition_number:
            new_pile_size += 1
        new_piles.append(new_pile_size)
    return new_piles

def split_unstable_piles(piles, stable_height, number_of_partitions):
    '''
    Split any unstable piles (piles > stable_height) into number_of_partitions
    '''
    split_piles = []
    for pile in piles:
        if pile > stable_height:
            new_piles = split_pile(pile, number_of_partitions)
            split_piles += split_unstable_piles(new_piles, stable_height, number_of_partitions)
        else:
            split_piles += [pile]
    return split_piles

starting_stack_size, max_stable_height, partition = map(int, input().split())

print(len(
    [pile for pile in split_unstable_piles([starting_stack_size], max_stable_height, partition)
        if pile != 0]
))   
        

assert split_pile(10, 5) == [2, 2, 2, 2, 2]
assert split_pile(8, 3) == [3, 3, 2]
assert split_pile(6, 7) == [1, 1, 1, 1, 1, 1, 0]

assert split_unstable_piles([13], 3, 2) == [2, 2, 3, 3, 3]
assert split_unstable_piles([3], 2, 5) == [1, 1, 1, 0, 0]
assert split_unstable_piles([1], 5, 4) == [1]
assert len(
        [pile for pile in split_unstable_piles([100], 1, 3) if pile != 0]
    ) == 100
assert len(
        [pile for pile in split_unstable_piles([64], 3, 2) if pile != 0]
    ) == 32
assert len(
        [pile for pile in split_unstable_piles([20], 3, 5) if pile != 0]
    ) == 20
