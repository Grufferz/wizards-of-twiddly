import pickle, gzip

def get_line(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    
    is_steep = abs(dy) > abs(dx)
    
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
        
    dx = x2 - x1
    dy = y2 - y1
    
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    
    y = y1
    points = []
    for x in range(x1, x2+1):
        coord = (y,x) if is_steep else (x,y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
        
    if swapped:
        points.reverse()
    
    return points


def save_object(obj, filename):
    with gzip.open(filename, 'wb') as output:
        pickle.dump(obj, output, 2)


def load_zip(filename):
    with gzip.open(filename, 'rb') as f:
        loaded = pickle.load(f)
        return loaded
