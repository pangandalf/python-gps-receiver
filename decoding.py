
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

def select_subframes_with_almanac(subframes):
    subframes_with_almanac = []
    for i in range(len(subframes)):
        subframe_num = int(subframes[i][49:52],2)
        satellite_num = int(subframes[i][62:68],2)

        if subframe_num == 4:
            if satellite_num in [2,3,4,5,7,8,9,10]:
                subframes_with_almanac.append(subframes[i])

        if subframe_num == 5 and satellite_num != 25:
            subframes_with_almanac.append(subframes[i])

    return subframes_with_almanac

def get_almanac_data(subframes_with_almanac):
    with open('almanac_data.txt', 'w') as f:
        f.write("")

    for subframe in subframes_with_almanac:

        words = get_words(subframe)

        subframe_num = int(words[1][19:22],2)
        satelite_num = int(words[2][2:8],2)

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
            f.write(f"                     (Subframe {subframe_num})\n")
            f.write(f"  1) Eccentricity: {eccentricity}\n")
            f.write(f"  2) Almanac reference time: {almanac_reference_time}\n")
            f.write(f"  3) Orbital inclination: {orbital_inclination}\n")
            f.write(f"  4) Rate of right ascension: {rate_of_right_ascension}\n")
            f.write(f"  5) Root of semi major axis: {root_of_semi_major_axis}\n")
            f.write(f"  6) Longitude of ascension node: {longitude_of_ascension_node}\n")
            f.write(f"  7) Argument of perigee: {argument_of_perigee}\n")
            f.write(f"  8) Mean anomaly at reference time: {mean_anomaly_at_reference_time}\n")
            f.write(f"  9) Clock bias: {clock_bias}\n")
            f.write(f"  10) Clock drift: {clock_drift}\n")

def decode(bitstream):
    indexes = find_preamble(bitstream)

    subframes = []
    for i in indexes:
        subframes.append(bitstream[i:i+300])

    pages_with_almanac = select_subframes_with_almanac(subframes)
    get_almanac_data(pages_with_almanac)

    with open('almanac_data.txt', 'r') as f:
        print(f.read())
