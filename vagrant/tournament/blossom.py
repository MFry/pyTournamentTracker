# exposed if deg(V') = 0
# augmentation path
# matching augmentation
# alternative path

'''
   INPUT:  Graph G, initial matching M on G
   OUTPUT: maximum matching M* on G
A1 function find_maximum_matching( G, M ) : M*
A2     P ← find_augmenting_path( G, M )
A3     if P is non-empty then
A4          return find_maximum_matching( G, augment M along P )
A5     else
A6          return M
A7     end if
A8 end function
'''