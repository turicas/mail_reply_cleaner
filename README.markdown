`mail_reply_cleaner`
==================

So you want to parse mail messages but do not want to have the reply lines?

Just try it:

```python

# coding: utf-8

from mail_reply_cleaner import clean_mail

my_message = u'''
this is a normal message

On 2012-10-22 <someone@mail> wrote:
> this text was answered
> so it'll be preserved

bla bla bla

On 2012-10-21 <other@mail> wrote:

> this text was answered too
> so it'll be preserved

spam eggs ham

On 2012-10-21 <other@mail> wrote:
> this reply was not answered
> so it'll be removed

--
my signature
multiline
it should be removed
'''

print clean_mail(my_message)
```

...and it'll print:

```
this is a normal message

On 2012-10-22 <someone@mail> wrote:
> this text was answered
> so it'll be preserved

bla bla bla

On 2012-10-21 <other@mail> wrote:

> this text was answered too
> so it'll be preserved

spam eggs ham
```
