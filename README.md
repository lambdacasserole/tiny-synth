# Tiny Synth
An experiment in synthesis of C code from a functional language.

The basic idea of this very simple and naive Python program is to transform a nameless functional language that looks a bit like this:

```
int,bin:int;
(add (rotate_right bin 1) (rotate_left (bitwise_and bin 1) 15)))
```

Into C code that can be compiled using [TinyC](http://bellard.org/tcc/).

## Structure
A specification file (`.spec` extension) is written in a nameless functional language with one function per file, with the function's name being the name of the file without extension. The basic structure of a specification file looks like this:

```
<return_type>,<param_name>:<param_type>;
<functional_code>
```

This includes the following:

* `<return_type>` - The return type of the C method to be generated.
* `<param_name>:<param_type>` - The name and type of each parameter to be included in the generated C method. Can be repeated arbitratily many times (comma-separated).
* `<functional_code>` - The functional code to compile as the body of the generated C method.

A primitive file (`.pc` extension) is written as a very small piece of C code with substitution placeholders for each argument of the function that corresponds to that primitive. For example `add.pc` contains this:

```
(%1 + %2)
```

## Reason
With functional programs being easier to reason about in general than imperative programs, I thought it'd a be a fun little experiment to try to synthesise some imperative code from functional code.

## Limitations
This isn't a serious development tool, and comes with some serious limitations and caveats. I'm sure there are a billion and one ways this could behave differently than expected.
