prac = "Faith is shown by deeds like the features of the face in a mirror. Discourses .."
source = "Discourses 29.4"

if source.find(r'\d+'):
    print(source)
    first_word = source.split(" ")[0]
    print(first_word)
    prac = prac.replace(" " + first_word + " ..", "")
    print(prac)
