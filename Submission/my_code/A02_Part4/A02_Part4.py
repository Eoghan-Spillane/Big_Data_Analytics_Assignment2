# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------

# ------------------------------------------
# IMPORTS
# ------------------------------------------
from socket import SOL_UDP
import pyspark
import pyspark.sql.functions

# ------------------------------------------
# FUNCTION my_main
# ------------------------------------------
def my_main(spark, my_dataset_dir, source_node):
    # 1. We define the Schema of our DF.
    my_schema = pyspark.sql.types.StructType(
        [pyspark.sql.types.StructField("source", pyspark.sql.types.IntegerType(), False),
         pyspark.sql.types.StructField("target", pyspark.sql.types.IntegerType(), False),
         pyspark.sql.types.StructField("weight", pyspark.sql.types.IntegerType(), False)
         ])

    # 2. Operation C1: 'read' to create the DataFrame from the dataset and the schema
    inputDF = spark.read.format("csv") \
        .option("delimiter", " ") \
        .option("quote", "") \
        .option("header", "false") \
        .schema(my_schema) \
        .load(my_dataset_dir)

    # ------------------------------------------------
    # START OF YOUR CODE:
    # ------------------------------------------------

    # Remember that the entire work must be done “within Spark”:
    # (1) The function my_main must start with the creation operation 'read' above loading the dataset to Spark SQL.
    # (2) The function my_main must finish with an action operation 'collect', gathering and printing by the screen the result of the Spark SQL job.
    # (3) The function my_main must not contain any other action operation 'collect' other than the one appearing at the very end of the function.
    # (4) The resVAL iterator returned by 'collect' must be printed straight away, you cannot edit it to alter its format for printing.

    # Type all your code here. Use as many Spark SQL operations as needed.
    # inputDF.show(50, False)
    inputDF.show()
    
    # Init Results Dataframe
    resultsDF = inputDF.select(inputDF.source.alias("id"), pyspark.sql.functions.lit("0").alias("cost"), pyspark.sql.functions.lit("").alias("path"))
    resultsDF = resultsDF.distinct().sort(resultsDF.id.asc())
    resultsDF = resultsDF.withColumn("path", pyspark.sql.functions.when(resultsDF.id == source_node, source_node).otherwise(""))
    resultsDF = resultsDF.withColumn("cost", pyspark.sql.functions.when(resultsDF.id != source_node, -1).otherwise(0))
    resultsDF.show(truncate = False)
    
    edge_candidites = inputDF.filter(inputDF.source == source_node) # Get possible edges
    edge_candidites.show(truncate = False)

    visited_nodes = resultsDF.select(resultsDF.id, pyspark.sql.functions.lit(False).alias("visited"))
    visited_nodes.show(truncate = False)

    while (len(edge_candidites.head(1)) > 0):
        
        #Get best edge candidate
        selected_candidate = edge_candidites.filter(edge_candidites.source == 1).sort(edge_candidites.weight.asc()).createOrReplaceTempView("selected_candidates")
        # cur
        spark.sql("Select * from selected_candidates").show()

        best_path = 

        
        
        quit()
        # def checkCandidites(x): 
        #     new_source_node = x[0][0]
        #     new_target_node = x[0][1]
        #     res = 

        # res = edge_candidites.foreach(lambda x: checkCandidites(x))

    # ------------------------------------------------
    # END OF YOUR CODE
    # ------------------------------------------------

    # Operation A1: 'collect' to get all results
    resVAL = solutionDF.collect()
    for item in resVAL:
        print(item)

# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now its time to apply this knowledge.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer finally processes this PYTHON PROGRAM EXECUTION section, which:
# (i) Specifies the function F to be executed.
# (ii) Define any input parameter such this function F has to be called with.
#
# --------------------------------------------------------
if __name__ == '__main__':
    # 1. We use as many input arguments as needed
    source_node = 1

    # 2. Local or Databricks
    local_False_databricks_True = False

    # 3. We set the path to my_dataset and my_result
    my_local_path = "../../"
    my_databricks_path = "/"

    my_dataset_dir = "my_datasets/my_dataset_3/"
    if local_False_databricks_True == False:
        my_dataset_dir = my_local_path + my_dataset_dir
    else:
        my_dataset_dir = my_databricks_path + my_dataset_dir

    # 4. We configure the Spark Session
    spark = pyspark.sql.SparkSession.builder.getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    print("\n\n\n")

    # 5. We call to our main function
    my_main(spark, my_dataset_dir, source_node)
