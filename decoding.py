def find_preamble(binary_string):

    indexes = []
    for i in range(len(binary_string) - 7):
        if binary_string[i:i+8] == '10001011':
            if i+300<len(binary_string) and binary_string[i+300:i+308] == '10001011':
                indexes.append(i)
                i += 300

    return indexes

def get_words(subframe):

    words = []
    for i in range(0, 300, 30):
        word = subframe[i:i+30]
        words.append(word)
    return words

def get_pages(subframes):

    pages = []
    for subframe in subframes:
        subframe_num = int(subframe[49:52],2)
        if subframe_num in [1,2,3]: continue

        pages.append(subframe)

    return pages

def get_pages_with_almanac(pages):
    
    pages_with_almanac = []
    for i in range(len(pages)):
        subframe_num = int(pages[i][49:52],2)
        if subframe_num == 4:
            if i!=len(pages)-1 and int(pages[i+1][62:68],2) in [2,3,4,5,7,8,9,10]:
                pages_with_almanac.append(pages[i])
                pages_with_almanac.append(pages[i+1])
                i += 1
            elif i==len(pages)-1 and int(pages[i-1][62:68],2) in [1,2,3,4,6,7,8,9]:
                pages_with_almanac.append(pages[i])
            continue

        if int(pages[i][62:68],2)!=25:
            pages_with_almanac.append(pages[i])
            
    return pages_with_almanac

def get_almanac_data(pages_with_almanac):

    with open('almanac_data.txt', 'w') as f:
        f.write("")

    for page in pages_with_almanac:

        words = get_words(page)

        subframe_num = int(words[1][19:22],2)
        page_num = int(words[2][2:8],2)

        if subframe_num == 4:
            indexes = [2,3,4,5,7,8,9,10]
            satelite_num = 25 + indexes.index(page_num)
        else:
            satelite_num = page_num

        eccentricity = int(words[2][8:24],2)
        almanac_reference_time = int(words[3][0:8],2)
        orbital_inclination = int(words[3][8:24],2)
        rate_of_right_ascension = int(words[4][0:16],2)
        root_of_semi_major_axis = int(words[5][0:24],2)
        longitude_of_ascension_node = int(words[6][0:24],2)
        argument_of_perigee = int(words[7][0:24],2)
        mean_anomaly_at_reference_time = int(words[8][0:24],2)
        clock_bias = int(words[9][0:8]+words[9][19:22],2)
        clock_drift = int(words[9][8:19],2)

        with open('almanac_data.txt', 'a') as f:
            f.write(f"\n----------------- Satelite number: {satelite_num} -----------------\n")
            f.write(f"\t\t (Subframe {subframe_num}, Page {page_num})\n")
            f.write(f"  1) Eccentricity: {eccentricity}\n")
            f.write(f"  2) Almanac reference time: {almanac_reference_time} [s]\n")
            f.write(f"  3) Orbital inclination: {orbital_inclination} [deg]\n")
            f.write(f"  4) Rate of right ascension: {rate_of_right_ascension} [deg/s]\n")
            f.write(f"  5) Root of semi major axis: {root_of_semi_major_axis} [1/sqrt(m)]\n")
            f.write(f"  6) Longitude of ascension node: {longitude_of_ascension_node} [deg]\n")
            f.write(f"  7) Argument of perigee: {argument_of_perigee} [deg]\n")
            f.write(f"  8) Mean anomaly at reference time: {mean_anomaly_at_reference_time} [deg]\n")
            f.write(f"  9) Clock bias: {clock_bias} [s]\n")
            f.write(f"  10) Clock drift: {clock_drift} [s/s]\n")

def decode(binary_string):

    indexes = find_preamble(binary_string)

    subframes = []
    for i in indexes:
        subframes.append(binary_string[i:i+300])

    pages = get_pages(subframes)
    pages_with_almanac = get_pages_with_almanac(pages)
    get_almanac_data(pages_with_almanac)

    with open('almanac_data.txt', 'r') as f:
        print(f.read())
