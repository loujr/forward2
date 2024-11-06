# Strongly vs Dynamic Languages
# Python is STRONGLY typed DYNAMIC language

# https://www.bairesdev.com/blog/static-vs-dynamic-typing/

# STATIC vs DYNAMIC
# For STATIC languages your IDE/build it will complain at COMPILE time if you're doing some
# kind of operand on incompatible types
# for DYNAMIC languages type checking is done at RUNTIME

# STRONG vs WEAKLY type
# A programing language that is strongly typed can either by dynamic or static
# Weakly-typed languages make conversions between unrelated types implicitly;
# whereas, strongly-typed languages don’t allow implicit conversions between unrelated types.

# JAVASCRIPT it is weakly typed and dynamic this will run without a single fucking error
# value = 21;
# value = value + "dot";
# console.log(value);
# 21dot

myName = "Lou " + 3 # We get a squiggle because we don't allow implicit type conversion

print(myName)
