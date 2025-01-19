using System;
using System.Collections.Generic;

public class StringParser
{
    public static List<string> ingredientParser(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return new List<string>();
        }

        List<string> initial = 



        return new List<string>(input.Split(';', StringSplitOptions.RemoveEmptyEntries));
    }

    public static List<string> stepParser(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return new List<string>();
        }

        List<string> initial = new List<string>(input.Split(';', StringSplitOptions.RemoveEmptyEntries));



        return ;
    }
}
