# sec. 1.5.5, page 19
# http://hplgit.github.io/prog4comp/doc/pub/p4c-sphinx-Python/._pylight002.html#formatting-text-and-numbers
real = 12.89643
integer = 42
string = 'some message'
print('real=%.3f, integer=%d, string=%s' % (real, integer, string))
print('real=%9.3e, integer=%5d, string=%s' % (real, integer, string))
