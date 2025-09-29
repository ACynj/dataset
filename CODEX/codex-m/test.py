def main(triplet_file):
    with open(triplet_file, "r", encoding="utf-8") as fin:
        for l in fin:
            u, r, v = l.split()
            print(u,r,v)
if __name__=="__main__":
    main("./test.txt")
