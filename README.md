# Final Project

## Sections:
1) Final Project Source code 
2) Data Storage
3) Generative Outputs


## Final Project Source code 

### How to Run?

The script needs one argument to run at the minimum and that must be the location of where you Data JSON Lives.
The second argument is used to determine if you want to generate additional data points using the other existing points as a reference.
The third and final argument is to specify a location so that a excel sheet can be generated with all the data that was ran.

### Example of how to run

1) Just get me my new P's and Q's
    <br/>python [Path]/Data.json<br/>
2) Generate X data points
    <br/>python [Path]/Data.json X<br/>
3) Generate X data points and create an excel sheet
    <br/>python [Path]/Data.json X [Path_to_storage]<br/>
4) Get me my new P's and Q's but don't generate data
<br/>python [Path]/Data.json 0 [Path_to_storage]<br/>

## Data Storage
### Why JSON?
Excel and CSV are very usual for storing data points, but in my personal experience with a JSON file
we can make the data more human readable. JSON will allow me to know that we are iterating over projects
with common fields, instead of having some files and manually filtering out columns or sections we don't need.
JSON allows us to have comments and in the future modify the code by looking for unique fields.
### How do I add data?
The Bread and Butter of the data is in the projects section which currently houses all projects that our 
hypothetical company currently utilizes. <br/><br/>

The following field(s) are needed in the JSON:
1) Environment Mode:
    <br/>i) Determines what type of software environment this is
    <br/>ii) Must be embedded, organic or semidetached<br/>

The following field(s) are needed in the JSON but can be left alone:
1) Generation Iterations
    <br/>i) Number of time to run the regression
    <br/>ii) If left at 0, the code will default to 100 times<br/>
2) Min SLOC 
    <br/>i) Minimum Range for the Lines of code that can be generated
    <br/>ii) Generated data cannot have SLOC lower than this value<br/>
3) Max SLOC
    <br/>i) MAX Range for the Lines of code that can be generated
    <br/>ii) Generated data cannot have SLOC greater than this value<br/>

The following field(s) are not currently supported:
1) Labor Hours in a Month
    <br/>i) Added for COCOMO but hasn't found a use yet<br/>

Each Project must have the following fields:
1) SLOC: Source Lines of Code (NOT KSLOC)
2) Development Time: The code will assume that any time you put in here is in YEARS
3) Effort: The code will assume that any effort you put in here is in YEARS
<br/>

## Generative Outputs

### Generate Data Points
The user can specify the number of data points they want to generate and relies on the already established data to generate some sort of output. The lines of code are chosen between a specified Min and Max found in the JSON, from there development time is calculated using a ratio of the SLOC to effort calculated from the already existing data and multiplying it by a random number anywhere from 0.90 to 1.10. Effort is calculated using the other established values.

### Generate Excel output
The user can specify a location where they can output a excel sheet if they so choose to, This excel sheet will be properly formatted and will have three sections. The first section on the left will be all the SLIM data from all project (even generated ones). The second of to the right will have AVERAGE and Variance calulated for specified fields. The final table on the bottom right will have R^2 values for certain comparison.