dots = []
folds = []

def count_dots(paper):
    return sum([(1 if paper[j][i] else 0) for i in range(len(paper[0])) for j in range(len(paper))])

with open('input') as f:
    while (row := f.readline().strip()) != '':
        coords = row.split(',')
        dots.append(tuple([int(x) for x in coords]))
    
    while (fold := f.readline().strip()) != '':
        folds.append((fold[11], int(fold[13:])))

max_x = max([coord[0] for coord in dots]) + 1
max_y = max([coord[1] for coord in dots]) + 1

paper = [[False] * (max_x) for _ in range(max_y)]

for x, y in dots:
    paper[y][x] = True

print('Before first fold:', count_dots(paper))

first_fold = True
for fold in folds:
    if fold[0] == 'x':
        fold_col = fold[1]
        fold_section = [row[fold_col + 1:] for row in paper]
        paper = [row[:fold_col] for row in paper]
        for y in range(len(fold_section)):
            for x in range(len(fold_section[0])):
                paper[y][-x-1] = paper[y][-x-1] or fold_section[y][x]
    else:
        fold_row = fold[1]
        fold_section = paper[fold_row + 1:]
        paper = paper[:fold_row]
        for y in range(len(fold_section)):
            paper[-y-1] = [(paper[-y-1][x] or fold_section[y][x]) for x in range(len(paper[0]))]
        
    if first_fold:
        print('After first fold:', count_dots(paper))
    first_fold = False

print('After last fold:', count_dots(paper))

for row in paper:
    print(''.join([('##' if row[i] else '  ') for i in range(len(row))]))
