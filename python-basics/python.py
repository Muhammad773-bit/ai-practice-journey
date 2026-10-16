""""Create a list of 3 filenames (e.g., ['data1.txt', 'data2.txt', 'data3.txt']).

Write a function process_ai_batch(file_list) that loops through these names.

Inside the loop, use a try-except block to open each file.

If the file exists, append its content to a master list called all_reviews.

If a file is missing, don't let the program crash. Instead, print: "Skipping [filename]: File not found."

Bonus: If a file is empty, raise a custom ValueError that says "File is empty"."""

file = ['data1.txt', 'data2.txt', 'data3.txt']
# make a function to process_ai_batch and loop through these names
def process_ai_batch(file):
    all_reviews = []
    try:
        for i in file:
            if i :
                i.append[all_reviews]
            else:
                print("file is not found")
    except:
        raise ValueError("file is empty")
    
    return all_reviews
            
process_ai_batch(file)