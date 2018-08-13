%%%Define int_pow
predicate int_pow( var int: x, var int: y, var int: r ) =
    let {
      array[ int, int ] of int: x2y = array2d( lb(x)..ub(x), lb(y)..ub(y),
        [ pow( X, Y ) | X in lb(x)..ub(x), Y in lb(y)..ub(y) ] )
    } in
      r == x2y[ x, y ];
