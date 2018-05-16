# Blast-Off*: Staph Annotation Pipeline
import os, webbrowser, pandas as pd, xlrd;  # Allows access to os commands, opening text files and manipulating Excel files
from selenium import webdriver; # Accesses the webdriver to open the web browser.
from selenium.webdriver.support.ui import Select;
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchWindowException; # Here and below are exceptions that the program will catch.
from selenium.common.exceptions import WebDriverException;
from selenium.common.exceptions import SessionNotCreatedException;
from selenium.common.exceptions import InvalidArgumentException;

class Ortholog_Report():
    
    def report(): # Creates the ortholog report.
        
        global report, report_name;
        
        report_name = input("\nEnter the name you want to use for the ortholog report: ");
        if report_name.endswith != '.txt': # Appends .txt to make the file into a text file.
            report_name = report_name + '.txt';
        
        create_report = open(report_name, 'w'); # Creates the file and makes it writable.
        create_report.close(); # Closes the file.
        report = open(report_name, 'r+'); # Opens the report and makes it both readable and writable.
        return; # Exits the function.
        
    def review(): # Final report.
        
        global report, report_name;
        
        report.write("\nNotes:"); #Writes to the ortholog report.
        report.close(); # Closes the report.
        
        webbrowser.open(report_name); # Opens the report text file.
        print("\nNow, please review the ortholog report for any discrepancies.", # Informs the user to look for any errors and to finalize the report.
              " Then, complete the report by giving it a Gene Name and add any notes about the gene. ",
              "Returning to the main menu.");
        return main(); # Exits to the main menu.
            
        
    def gene_ID(id_file): # Creates a default gene ID.
        
        global report;
        
        sequence = id_file[0:10]; # Shortens the name of the Excel file to make the default gene ID.
        choice = input("\nDo you want the gene name to be " + sequence + "? Enter(y/n): "); # Asks the user if they want to use the default name.
        
        if choice == 'y' or choice == 'Y': # Keeps the default name.
            report.write("geneID: " + sequence + "\ngeneName: "); # Writes the gene ID into the ortholog report.
        elif choice == 'n' or 'N': # Allows the user to create their own default name.
            sequence = input("\nEnter the gene name: ");
            report.write("geneID: " + sequence + "\ngeneName: "); # Writes the gene ID into the ortholog report.
        else: # Input validation.
            print("\nThat isn't an option. Try again.") 
            
        return; # Exits the function.
    
    def get_allele_frequency(sheet, identity, df): # Gets the number of alleles in the Excel file.
        
        global report;
        match = 0;
        for row in range(sheet.nrows): # Checks the Excel file for the number of alleles.
            if sheet.cell_value(row, 3) >= identity:
               match = match + 1;
               identity_count = df['d'].value_counts().to_dict();
               
        alleles = len(identity_count);
        report.write("\ngenomes_matched: " + str(match) + "\nIdentity_threshold: " + str(identity) + "\nalleles: " + str(alleles)); # Writes to the ortholog report.
        return Ortholog_Report.list_of_matching_protein(sheet, identity);
     
    def list_of_matching_protein(sheet, identity):
        
        global driver;
        match_file = input("\nEnter the name you want to use for the list of matching proteins: "); # Name the list of matching proteins.
        
        if match_file.endswith != '.txt':  # Adds the extension .txt if it isn't there already.
           match_file = match_file + '.txt';
        
        matches = open(match_file, 'w+'); # Creates the file for the list of matching proteins and makes it both readable and writable.
            
        for row in range(sheet.nrows): # Writes the list of matching to a text file.
            if sheet.cell_value(row, 3) >= identity:
                matches.write("\n" + str(sheet.cell_value(row, 1)));
                
        matches.close();
        
        file_directory = open("default_directory.txt", 'r'); # Opens the default directory text file as readable.
        key = file_directory.read(); # Read the default_directory text file.
        workflow.batch(key, match_file);
        file_directory.close(); # Closes the default directory text file.
            
        workflow.align(key); 
        workflow.show_align(key);
        
        return Ortholog_Report.review(); # Review and finish the ortholog report.
        
        
class files():
    
    def set_default_directory():
        
        choice = input("\nDo you want to set a default directory? (y/n): ")
        if choice == 'y' or choice == 'Y':
            if os.path.exists('default_directory.txt') and os.stat('default_directory.txt').st_size != 0: # Checks if the file exists and if it is not empty.
                default = open('default_directory.txt', 'r+'); # Opens the default directory text file as readable.
                print("The current default directory is: " + str(default.read())); # Prints the name of the default directory.
            elif os.path.exists('default_directory.txt') and os.stat('default_directory.txt').st_size == 0: # Checks if the file exists and if it is empty.
                default = open('default_directory.txt', 'r+'); # Opens the default directory text file as readable.
                print("\nThere is no default directory."); # Prints that there is no default directory.
            else: # If the default directory text file doesn't exist.
                default = open('default_directory.txt', 'w+'); # Creates the default directory text file.
                print("\nThere is no default directory."); # Prints taht there is no default directory.
        
        elif choice == 'n' or choice == 'N': # Returns to the main menu.
            print("\nReturning to the main menu.\n");
            return main();
        
        else: # Input validation.
            print("\nThat isn't an option. Try again.");
            files.set_default_directory(); # Retry.
            
        change = input("\nPlease enter the default directory you want to use: "); # Asks the user to enter what directory they want to use.

        if os.path.exists(change) == True: # Checks if the directory exists.
            os.chdir(change); # Changes the directory.
            default.seek(0); # Reads the whole text file.
            default.truncate(); # Erases the data in the text file.
            default.write(change); # Writes the new default directory into the text file.
            default.close(); # Closes the text file.
            return main();
        
        else: # If the directory doesn't exists.
            default.close(); # Closes the text file.
            print("\nThis directory doesn't exist...");
            return main();
        
    def change_directory():
        
        if os.path.exists('default_directory.txt'): # Checks if the default directory text file exists.
            default = open('default_directory.txt', 'r'); # Opens the default directory text file as readable.
            print("\nThe current default directory is: " + str(default.read())); # Prints the name of the default directory.
            default.close(); # Closes the text file.

        else: # If the default directory text file doesn't exist.
            print("\nThe current directory is: " + str(os.getcwd())); # Prints the current working directory instead.
        
        change = input("\nPlease enter the directory you want to use: "); # Asks the user what directory they want to use.

        if os.path.exists(change) == True: # Checks if the directory exists.
            os.chdir(change); # Changes the directory.
        elif os.path.exists(change) == False: # If the directory doesn't exist.
            print("\nThis directory doesn't exist...");

        return;
                
    def make_folder():
        
        choice = input("\nDo you want to create folder in a different directory? (y/n): "); # Asks the user if they want to create the folder in a different directory.
        
        if choice == 'y' or choice == 'Y': # Changes the directory.
            files.change_directory();
        elif choice == 'n' or choice == 'N': # Remain the current directory.
            print("\nThe file will me made in the current directory: " + str(os.getcwd())  + "\n"); # Prints the name of the current working directory.
            
        name = input("\nPlease enter the name of the folder: "); # Enter the name of the folder.

        if name == 'm' or name == 'M': # To return to the main menu.
            print("\nReturning to the main menu.");
        elif not os.path.exists(name): # If the folder doesn't already exist, create the folder.
            os.makedirs(name);
        else: # If the folder already exists.
            print("\nThat folder already exists in this directory!");
            
        return main(); # Returns to the main menu.
    
    def open_text_file(file_name):
        
        if os.path.exists(file_name) == True: # If the file exists, open it.
            webbrowser.open(file_name);
        else: 
            print("\nThis file doesn't exist...");
            
        return main(); # Returns to the main menu.
        
    def view_directory(): # Lists the contents of the current directory.
        
        print("\nThis directory contains: " + str(os.listdir()));

class excel_manipulation():
    
    def load_excel_file(file):
        
        global driver;
        
        xl = pd.ExcelFile(file); # Loads the Excel file in Pandas.
        worksheet = xl.sheet_names[0]; # Access sheet 0.
        workbook = xlrd.open_workbook(file) # Loads the Excel file in xlrd.
        work = workbook.sheet_by_name(worksheet) # Access sheet 0.
            
        df = pd.read_excel(xl, worksheet); # Reads the Excel file.
        df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        genomes = len(df)+1; # The number of genomes start at 1.

        print("\nThis excel file contains " + str(genomes) + " rows."); # Prints the number of genomes.
        cell1 = work.cell_value(rowx=0,colx=0); #Checks the value of the cells to get the worst matches after sorting.
        cell2 = work.cell_value(rowx=0,colx=1);
        input("\nPlease sort this file within Excel. Once completed, save the excel file and press enter"); # Prompts the user to sort the Excel file.
        print("\nThe next few steps will require the use of a web browser. After pressing enter, You will get a prompt asking if you want to give this program access."  
              , "If you don't want this program to open a web browser, decline the prompt, which will print the link to the website so you can manually complete the step.")
        input("Press enter to continue");
        
        workflow.blast(cell1, cell2);
        
        cut_off = input("\nPlease enter the cutoff: ");
        cut_off = float(cut_off); # Changes the cut off to a float.
        Ortholog_Report.get_allele_frequency(work, cut_off, df);
                

    def choose_excel_file():
        
        file = input("\nWhich file do you want to open in Microsoft excel (include the extention 'xlsx')? Enter wd to return to the previous step or v to view the contents of the directory: ");
        
        if os.path.exists(file):# and file.endswith == '.xlsx':
            print("\nYou entered: " + file);
        
        elif os.path.exists(file) == False and os.path.exists(file + ".xlsx") == True: # If the given file doesn't exist, but it does with the extension added.
            file = file + ".xlsx";
            print("\nYou entered: " + file);
            
        elif file == 'wd': # Go back and change the directory.
            return workflow.working_directory();
            
        elif file == 'v': # View the contents of the current directory.
            files.view_directory();
            excel_manipulation.choose_excel_file();
            
        else: # If the file doesn't exist.
            print("\nThis file doesn't exist in this directory! Did you add the extension '.xlsx'?");
            excel_manipulation.choose_excel_file();
            
        choice = input("\nIs this correct? Enter(y/n): ");

        if choice == 'y' or choice == 'Y': # if it is the right file.
            Ortholog_Report.gene_ID(file); # Give Gene ID.
        elif choice == 'n' or choice == 'N': # If it is not the right file.
            print("\nTry again.");
            excel_manipulation.choose_excel_file(); # Retry.
            
        else:
            print("\nThat isn't an option! Try again.");
            excel_manipulation.choose_excel_file();
            
        return excel_manipulation.load_excel_file(file);

class workflow():
    
    def working_directory():
        
        cont = 0;
        if os.path.exists('default_directory.txt') and os.stat('default_directory.txt').st_size != 0: # Checks if the default directory file exists and if its not empty.
            default = open('default_directory.txt', 'r'); # Open the default directory file as read.
            os.chdir(str(default.read())); # Reads the default directory text file and change the directory to the default directory.
        else:
            print("\nThe set default directory doesn't exist. You may return to the main menu and set a new default directory,", 
                  "otherwise we'll use the current directory.");
            create_default = open('default_directory.txt', 'w+'); # Creates a default directory text file if it doesn't exist.
            create_default.write(str(os.getcwd())); # Writes the current working directory as the default.
            create_default.close(); # Closes the file.
    
        while cont != 1:
            print("\n------------\nBlast-off *\n------------\nThe current directory is: " + str(os.getcwd())+ "\nTo return to the main menu,",
                  " enter(m). To view items in this directory, enter(v). To create a folder, enter(mf). To view the workflow, enter(wf).");
            choice = input("\nDo you want to work in this directory? Enter(y/n): ");
        
            if choice == 'y' or choice == 'Y':
                cont = 1; # Exits the loop
                Ortholog_Report.report(); # Creates the ortholog report
                excel_manipulation.choose_excel_file();  # Choose an Excel file.
            
            elif choice == 'n' or choice == 'N':
                files.change_directory(); # Allows the user to change the directory.
            
            elif choice == 'm' or choice == 'M': # Return to the main menu.
                cont = 1; # Exit the loop
                return main(); # Return to the main menu.
            
            elif choice == 'v' or choice == 'V': # View the contents of the current directory.
                files.view_directory(); # Shows current directory
                workflow.working_directory(); # Starts at the beginning of the function.
           
            elif choice == 'mf':
                files.make_folder(); # Creates a new folder.
            
            elif choice == 'wf':
                files.open_text_file("research_workflow.txt"); # Opens the workflow textfile.
            
            else:
                print("That isn't an option! Try again."); # Input validation.
                workflow.working_directory();
        
    
    def webbrowser(link):
        
        global driver;
        
        browser = input("\nDo you want to use: \n1) Google Chrome\n2) Firefox\n:");

        if browser == '1':
            try: # If any of these above errors occur, then Google Chrome will be used.
                driver = webdriver.Chrome(executable_path=r"chromedriver.exe");
                driver.get(link);
            except (SessionNotCreatedException, NoSuchWindowException, WebDriverException, InvalidArgumentException) as error: # Error handling.
                print("\nThe webpage was unable to be open. The link to the website is: " + link); # Prints out if none of the browsers work.
                input("\nCopy and paste the link into your webbrowser and complete this step manually. Press enter once this step is completed");
                pass;

        elif browser == '2':
            try: # Attempts to open the web page using Firefox.
                driver = webdriver.Firefox();
                driver.get(link);

            except (SessionNotCreatedException, NoSuchWindowException, WebDriverException, InvalidArgumentException) as error: # Error handling.
                print("\nThe webpage was unable to be open. The link to the website is: " + link); # Prints out if none of the browsers work.
                input("\nCopy and paste the link into your webbrowser and complete this step manually. Press enter once this step is completed");
                pass;
            
        else:
            print("\nThat isn't an option. Try again.");
            workflow.choose_browser();
                
    def blast(cell1, cell2):
        
        workflow.webbrowser("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins&PROGRAM=blastp&BLAST_PROGRAMS=blastp&PAGE_TYPE=BlastSearch&BLAST_SPEC=blast2seq&DATABASE=n/a&QUERY=&SUBJECTS=");
        
        inputElement1 = driver.find_element_by_id("seq"); # Looks for elements.
        inputElement2 = driver.find_element_by_id("subj");

        inputElement1.send_keys(cell1); # Inputs the data.
        inputElement2.send_keys(cell2);
    
    def batch(key, match_file):
        
        workflow.webbrowser("https://www.ncbi.nlm.nih.gov/sites/batchentrez"); # Opens the website.
        
        try:
            element1 = driver.find_element_by_name("file"); # Looks for the element. 
            element1.send_keys(key + "/" + match_file); # Inputs the data.
            element2 = Select(driver.find_element_by_name("db")); # Looks for the element.
            element2.select_by_value("protein"); # Changes the value to protein.
        except (InvalidArgumentException) as error: # If the data isn't input correctly.
            print("\nError! We are unable to upload the data. You must do it manually.")
            input("\nPress enter to continue once the step is completed.");
            pass;
    
    def align(key):
        
        alignment = input("\nOnce you've completed step 9, enter the name of the FASTA file: "); # Input the FASTA file.
        
        if os.path.exists(alignment): # Checks if the file exists.
            print("\nYou entered: " + alignment); # Prints the file name.
        elif os.path.exists(alignment) == False and os.path.exists(alignment + '.fasta'): # Adds the .fasta extension if it isn't already there.
            alignment = alignment + '.fasta'; 
        else: # Input validation.
            print("\nThis file doesn't exist. Try again.");
            workflow.align(key); 

        try: # Attempts to open the website in the web browser.
            workflow.webbrowser("https://www.ebi.ac.uk/Tools/msa/clustalo");
            element3 = driver.find_element_by_name("upfile");
            element3.send_keys(key + "/" + alignment);
            element3.submit();
        except (InvalidArgumentException) as error: # If there is an input error, this will print.
            print("\nError! We are unable to upload the data. You must do it manually.")
            input("\nPress enter to continue once the step is completed.");
            pass;
        
    def show_align(key):
        show_align = input("\nEnter the name of the multiple alignment file that you want to show align: ")
        
        if os.path.exists(show_align): # Checks if the file exists.
            print("\nYou entered: " + show_align); # Prints the files name.
        elif os.path.exists(show_align) == False and os.path.exists(show_align + '.txt'): # Adds the .txt extension if it isn't already there.
            show_align = show_align + '.txt';
        else: # Input validation.
            print("\nThis file doesn't exist. Try again.");
            workflow.show_align(key); 
        try: # Attemps to open the website in the web browser.
            workflow.webbrowser("http://www.bioinformatics.nl/cgi-bin/emboss/showalign");
            element4 = driver.find_element_by_name("sequence.file");
            element4.send_keys(key + "/" + show_align);
        except (InvalidArgumentException) as error: # Checks for any input errors.
            print("\nError, we are unable to upload the data. You must do it manually.")
            input("\nPress enter to continue once the step is completed.");
            pass;

"""    def choose_browser():
        browser = input("\nDo you want to use: \n1) Google Chrome\n2) Firefox\n:");

        if browser == '1':
            

        elif browser == '2':
            

        else:
            print("\nThat isn't an option. Try again.");
            workflow.choose_browser(); """
            
            
            
def main(): # Main menu 
    print("  __   __        __      ____   _____        ______  _____  ______\n",
    "|  \ |  |      /  \    /   _| |_   _| ___  |  __  || ____/| ____/ \n",
    "|--< |  |__   / /\ \   \  \     | |  |___| | |__| || ___/ | ____/ \n",
    "|__/ |_____| / /  \ \ /____\    | |	    |______||_|    |_| \n",
    "-----------------------------------------------------------------")
    

    choice = input("1)Start\n2)Set default directory\n3)View Research Workflow\n4)Create a folder\n5)Exit\nSelect: ");

    if choice == '1':
        workflow.working_directory(); # Starts the program.
    elif choice == '2':
        files.set_default_directory(); # Setting the default directory.
    elif choice == '3':
        files.open_text_file("research_workflow.txt"); # Opens the workflow text file.
    elif choice == '4':
        files.make_folder(); # Creates a new folder in the current directory.
    elif choice == '5':
        exit(0); #Exits the program.
    else:
        print("That isn't an option! Try again."); # Input validation.
        main(); # Returns to the main menu.

if __name__=='__main__':
    main();
