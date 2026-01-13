def __create_middle_row(self, row1, row2):
    middle_row = {}
    for key in row1:
        # to do: genericity
        if key == "Beach Name":
                middle_row[key] = row1[key]
        # to do: genericity
        if key == "Measurement Timestamp":
                middle_row[key] = ""
        else:
            if row1[key] == "" and row2[key] == "":
                    middle_row[key] = ""
            if row1[key] != "" and row2[key] != "":
                    middle_row[key] =  round( ( float(row1[key]) + float(row2[key]) )/2 , 3 )
    return middle_row
                      
    
def _add_missing_rows(self, chunk, common_difference, max_approximated, time_source_column):

    act = chunk[0][time_source_column]
    new_rows = [act]

    for row in chunk:
        next = row[time_source_column]
        dif = abs(act[time_source_column] - next[time_source_column])
        
        if dif <= common_difference:
            new_rows.append(row)
            act = row
            continue

        if max_approximated < dif:
            new_rows.append(row)
            act = row
            continue
        
        middle_row = self._create_middle_row(act, next)
        act_time = act[time_source_column]
        number_of_missing_rows = dif%common_difference

        for j in range(number_of_missing_rows):
                middle_row[time_source_column] = act_time + j*common_difference
                new_rows.append(middle_row)

        new_rows.append(next)            
        prev = act

    return new_rows
