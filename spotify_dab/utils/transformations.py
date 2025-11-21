#try use Class << transformations>> to drop columns
class transformations:

    def dropCol(self,df,columns):
        df=df.drop(*columns)
        return df
