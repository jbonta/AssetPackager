import copy
import os
import re
import urllib2
from subprocess import Popen, PIPE, STDOUT

YUI_COMMAND = 'yuicompressor'.split(' ')

SEP = '|||'
rSEP = '\|\|\|' # for some reason I only needed single backslashes, unlike re.escape
fulltoken_re = re.compile('^(?:.*?)(%s)(.*)(%s)(?:.*?)$' % (rSEP, rSEP))
localpath_re = re.compile('^(?!http|\/\/)')

def _shift(queue):
  if not queue:
    return None
  shifted = queue[0]
  del queue[0]
  return shifted

# remove needle from the middle of array[index], putting back what's on either side of needle
# as separate elements
# _splitArray([0,0,['a', 'b', 'c'], 0 0], 2, ['b'])
#   => [0,0,['a'], ['c'], 0 0]
def _splitArray(array, index, needle):
  haystack = array[index]
  # find needle in haystack:
  pos = [x for x in xrange(len(haystack)) if haystack[x:x+len(needle)] == needle][0]
  before, after = haystack[:pos], haystack[pos + len(needle):]
  del array[index]
  if after:
    array.insert(index, after)
  if before:
    array.insert(index, before)

# just longest common substring routine with a serialize/deserialize step at beginning/end
def longest_common_subarray(a1, a2):
  a1, a2 = SEP + SEP.join(a1) + SEP, SEP + SEP.join(a2) + SEP
  m = [[0] * (1 + len(a2)) for i in xrange(1 + len(a1))]
  longest, x_longest = 0, 0
  for x in xrange(1, 1 + len(a1)):
    for y in xrange(1, 1 + len(a2)):
      if a1[x - 1] == a2[y - 1]:
        m[x][y] = m[x - 1][y - 1] + 1
        if m[x][y] > longest:
          longest = m[x][y]
          x_longest = x
      else:
        m[x][y] = 0
  result = a1[x_longest - longest: x_longest]
  matches = re.search(fulltoken_re, result)
  return matches.group(2).split(SEP) if matches else []

def _isLocalFile(path):
  return re.match(localpath_re, path)




# Given a list of asset paths grouped by page, return a list of lists, basically
# a bucketed version based on usage commonality.
def analyze(assets):
  queue = copy.copy([i for i in assets if i])
  result = [_shift(queue)] if len(queue) else []
  while len(queue):
    for i, result_chunk in enumerate(result):
      sub = longest_common_subarray(result_chunk, queue[0])
      if len(sub):
        _splitArray(queue, 0, sub)
        if len(sub) != len(result_chunk):
          _splitArray(result, i, sub)
          result.insert(i, sub)
        break
    else:
      result.append(_shift(queue))
  return result

# Given a list of paths (local or remote), concatenate them together and save
# locally as output.
def package(input_list, output, compress=True, filename_markers_in_comments=True):
  out = open(output, 'w') # clear contents
  out = open(output, 'a')
  for i, in_file in enumerate(input_list):
    if i != 0:
      out.write('\n\n' if filename_markers_in_comments else '\n')
    if filename_markers_in_comments:
      in_file_short = os.path.basename(in_file)
      out.write('/* %s %s */\n' % (in_file_short, '-' * 40))
    out.flush()

    if _isLocalFile(in_file):
      cmd = YUI_COMMAND if compress else ['cat']
      Popen(cmd + [in_file], stdout=out).wait()
    else:
      if in_file.startswith('//'):
        in_file = 'http:' + in_file
      file_type = 'js' if in_file.endswith('js') else 'css'
      cmd = YUI_COMMAND + ['--type=' + file_type] if compress else ['cat']
      p = Popen(cmd, stdout=out, stdin=PIPE, stderr=STDOUT)
      p.communicate(input=urllib2.urlopen(in_file).read())
