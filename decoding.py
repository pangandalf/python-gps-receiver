def find_preamble(bitstream):

    indexes = []
    for i in range(len(bitstream) - 7):
        if bitstream[i:i+8] == '10001011':
            if i+300<len(bitstream) and bitstream[i+300:i+308]=='10001011':
                indexes.append(i)
                i += 300

    return indexes

def get_words(subframe):

    words = []
    for i in range(0, 300, 30):
        word = subframe[i:i+30]
        words.append(word)
    return words

def select_subframes(subframes):

    select_subframes = []
    for subframe in subframes:
        subframe_num = int(subframe[49:52],2)
        if subframe_num in [1,2,3]: continue

        select_subframes.append(subframe)

    return select_subframes

def select_subframes_with_almanac(subframes):
    
    subframes_with_almanac = []
    for i in range(len(subframes)):
        subframe_num = int(subframes[i][49:52],2)
        if subframe_num == 4:
            if i!=len(subframes)-1 and int(subframes[i+1][62:68],2) in [2,3,4,5,7,8,9,10]:
                subframes_with_almanac.append(subframes[i])
                subframes_with_almanac.append(subframes[i+1])
                i += 1
            elif i==len(subframes)-1 and int(subframes[i-1][62:68],2) in [1,2,3,4,6,7,8,9]:
                subframes_with_almanac.append(subframes[i])
            continue

        if int(subframes[i][62:68],2)!=25:
            subframes_with_almanac.append(subframes[i])
            
    return subframes_with_almanac

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

def decode(bitstream):

    indexes = find_preamble(bitstream)

    subframes = []
    for i in indexes:
        subframes.append(bitstream[i:i+300])

    pages = select_subframes(subframes)
    pages_with_almanac = select_subframes_with_almanac(pages)
    get_almanac_data(pages_with_almanac)

    with open('almanac_data.txt', 'r') as f:
        print(f.read())
