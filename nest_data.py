import pandas as pd
import datetime
import argparse
import json
import pyperclip

def main(data, start_time):
    df = pd.DataFrame(data, columns=["StartTime", "EndTime"])
    df = calculate_datetime(df, start_time)
    out_df = generate_data(df)
    out_df = final_form(out_df)
    dt = [z for z in out_df.to_string(index=False, header=False, col_space=0).split(" ") if z != '']
    dt.insert(0, start_time.strftime("%m/%d/%Y"))
    pyperclip.copy("\t".join(dt))


def calculate_datetime(df, start_time):
    df["StartTime_DT"] = df["StartTime"].apply(lambda x: start_time + datetime.timedelta(minutes=(x*(24*60))))

    def calc_v(row):
        return row["StartTime_DT"] + datetime.timedelta(minutes=(row["EndTime"]*(24*60)))
    df["EndTime_DT"] = df.apply(calc_v, axis=1)
    return df


def calculate_hour_values(start_time, end_time):
    pd.date_range(start_time, end_time, freq='h')
    rng = pd.date_range(start_time.floor('h'), end_time.floor('h'), freq='h')

    # get the left and right endpoints for each hour
    # clipped to be inclusive of [start_time, end_time]
    left = pd.Series(rng, index=rng).clip_lower(start_time)
    right = pd.Series(rng + 1, index=rng).clip_upper(end_time)

    # construct a series of the lengths
    y = right - left
    return y.to_frame().reset_index().rename(columns={'index':"DT", 0: "Length"})

def generate_data(df):
    frm = pd.DataFrame(columns=["DT", "Length"])
    for i in df.itertuples():
        start_time = i[3]
        end_time = i[4]
        frm = frm.append(calculate_hour_values(start_time, end_time))
    frm_gp = frm.groupby("DT").sum()
    frm_gp["Length"] = frm_gp["Length"].apply(lambda x: x.seconds/60)
    frm_gp.insert(0, "Hour", frm_gp.index.hour)
    return frm_gp


def final_form(df_final):
    frmx = pd.DataFrame(data=[[x] for x in range(0,24)], columns=["Hour"])
    frmx = frmx.set_index("Hour")
    df_final = df_final.set_index("Hour")
    frm_final = frmx.join(df_final)
    frm_final["Length"].loc[pd.isnull] = 0
    frm_final = frm_final.groupby("Hour").sum().transpose()
    return frm_final



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('date', type=str,                        
                        help='Date Value formatted like yyyy/mm/dd - 2018/06/12')    
    args = parser.parse_args()
    data = pyperclip.paste()
    data = json.loads(data)
    if type(data) is str:
        data = json.loads(data)
    date_value = datetime.datetime.strptime(args.date, "%Y/%m/%d")
    main(data, date_value)