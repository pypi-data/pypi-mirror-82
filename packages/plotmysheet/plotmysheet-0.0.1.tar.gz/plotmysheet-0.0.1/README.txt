This is a very simple library that allow the user to plot the graph between the two columns of
the google spreadsheet.
To get the graph you are provided by two methods two methods :

1) get_all_columns(url): In this method you have to provide the url of the the google sheet and it will return the list of 
   all the columns of your sheet.

2) plot_graph(url,column1,column2,path="assets") : Now to plot the graph you are provided with plot graph method.In
   this method you have to provide the url of the googlesheet and you respective column1 number i.e if it is column 1 then
   you have provide only "1" as its value and the same concept will be applied with column2 value and at last if you
   want to store your graph image then you must have folder names as assets, where it will store the my_plot.png image of the graph.

Things to be taken Care of :

1) Both column 1 and column 2 value should be numeric.
2) Google sheet link should be valid.