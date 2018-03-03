# Blast-Off*: Staph Annotation Pipeline
import os, webbrowser, pandas as pd, xlrd;
from selenium import webdriver;
from selenium.webdriver.support.ui import Select;
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchWindowException;
from selenium.common.exceptions import WebDriverException;
from selenium.common.exceptions import SessionNotCreatedException;

class Ortholog_Report():
    def report():
        global report, report_name;
        
        report_name = input("\nEnter the name you want to use for the ortholog report: ");
        if report_name.endswith != '.txt':
            report_name = report_name + '.txt';
        
        create_report = open(report_name, 'w');
        create_report.close();
        report = open(report_name, 'r+');
        return;
        
    def review():
        global report, report_name;
        
        report.write("\nNotes:");
        report.close();
        
        webbrowser.open(report_name);
        print("\nNow, please review the ortholog report for any discrepancies.", 
              " Then, complete the report by giving it a Gene Name and add any notes about the gene. ",
              "Returning to the main menu.");
        return main();
            
        
    def gene_ID(id_file):
        global report;
        
        sequence = id_file[0:10]; 
        choice = input("\nDo you want the gene name to be " + sequence + "? Enter(y/n): ");
        
        if choice == 'y' or choice == 'Y':
            report.write("geneID: " + sequence + "\ngeneName: ");
        elif choice == 'n' or 'N':
            sequence = input("\nEnter the gene name: ");
            report.write("geneID: " + sequence + "\ngeneName: ");
        else:
            print("\nThat isn't an option. Try again.")
            
        return;
    
    def get_allele_frequency(sheet, identity, match):
        global report;
        
        alleles = 0;
        for row in range(sheet.nrows):
            if sheet.cell_value(row, 3) >= identity:
                alleles = alleles + 1;
        
        report.write("\ngenomes_matched: " + str(match) + "\nIdentity_threshold: " + str(identity) + "\nalleles: " + str(alleles));
        return Ortholog_Report.list_of_matching_protein(sheet);
     
    def list_of_matching_protein(sheet):
        global driver;
        match_file = input("\nEnter the name you want to use for the list of matching proteins: ");
        
        if match_file.endswith != '.txt':
            match_file = match_file + '.txt';
        
        matches = open(match_file, 'w+');
            
        for row in range(sheet.nrows):
            matches.write("\n" + str(sheet.cell_value(row, 1)));
        matches.close();
        
        file_directory = open("default_directory.txt", 'r');
        key = file_directory.read();
        workflow.batch(key, match_file);
        file_directory.close();
            
        workflow.align(key);
        workflow.show_align(key);
        
        return Ortholog_Report.review();
        
        
class files():
    def set_default_directory():
        if os.path.exists('default_directory.txt') and os.stat('default_directory.txt').st_size != 0:
            default = open('default_directory.txt', 'r+');
            print("The current default directory is: " + str(default.read()));
        elif os.path.exists('default_directory.txt') and os.stat('default_directory.txt').st_size == 0:
            default = open('default_directory.txt', 'r+');
            print("\nThere is no default directory.");
        else:
            default = open('default_directory.txt', 'w+');
            print("\nThere is no default directory.");
            
        change = input("\nPlease enter the default directory you want to use: ");

        if os.path.exists(change) == True:
            os.chdir(change);
            default.seek(0);
            default.truncate();
            default.write(change);
            default.close();
            return main();
        
        else:
            default.close();
            print("\nThis directory doesn't exist...");
            return main();
        
    def change_directory():
        if os.path.exists('default_directory.txt'):
            default = open('default_directory.txt', 'r');
            print("\nThe current default directory is: " + str(default.read()));
        
        else:
            print("\nThe current directory is: " + str(os.getcwd()));
        
        change = input("\nPlease enter the directory you want to use: ");

        if os.path.exists(change) == True:
            os.chdir(change);
        
        elif os.path.exists(change) == False:
            print("\nThis directory doesn't exist...");
        
        default.close();
        return;
                
    def make_folder():
        files.change_directory();
        name = input("\nPlease enter the name of the folder: ");

        if name == 'm' or name == 'M':
            print("\nReturning to the main menu.");
        elif not os.path.exists(name):
            os.makedirs(name);
        else:
            print("\nThat folder already exists in this directory!");
            
        return main();
    
    def open_text_file(file_name):
        if os.path.exists(file_name) == True:
            webbrowser.open(file_name);
        else:
            print("\nThis file doesn't exist...");
            
        return main();
        
    def view_directory():
        print("\nThis directory contains: " + str(os.listdir()));        

class excel_manipulation():
    def load_excel_file(file):
        global driver;
        xl = pd.ExcelFile(file);
        worksheet = xl.sheet_names[0];
        workbook = xlrd.open_workbook(file)
        work = workbook.sheet_by_name(worksheet)
            
        df = pd.read_excel(xl, worksheet);
        genomes = len(df)+1;

        print("\nThis excel file contains " + str(genomes) + " rows.");
        cell1 = work.cell_value(rowx=0,colx=0);
        cell2 = work.cell_value(rowx=0,colx=1);
        input("\nPlease sort this file within Excel. Once completed, save the excel file and press enter");
        print("\nThe next few steps will require the use of a web browser. After pressing enter, You will get a prompt asking if you want to give this program access."  
              , "If you don't want this program to open a web browser, decline the prompt, which will print the link to the website so you can manually complete the step.")
        input("Press enter to continue");
        
        workflow.blast(cell1, cell2);
        
        cut_off = input("\nPlease enter the cutoff: ");
        cut_off = float(cut_off)
        Ortholog_Report.get_allele_frequency(work, cut_off, genomes);
                

    def choose_excel_file():
        
        file = input("\nWhich file do you want to open in Microsoft excel (include the extention 'xlsx')? Enter wd to return to the previous step or v to view the contents of the directory: ");
        
        if os.path.exists(file):# and file.endswith == '.xlsx':
            print("\nYou entered: " + file);
        
        elif os.path.exists(file) == False and os.path.exists(file + ".xlsx") == True:
            file = file + ".xlsx";
            print("\nYou entered: " + file);
            
        elif file == 'wd':
            return workflow.working_directory();
            
        elif file == 'v':
            files.view_directory();
            excel_manipulation.choose_excel_file();
            
        else:
            print("\nThis file doesn't exist in this directory! Did you add the extension '.xlsx'?");
            excel_manipulation.choose_excel_file();
            
        choice = input("\nIs this correct? Enter(y/n): ");

        if choice == 'y' or choice == 'Y':
            Ortholog_Report.gene_ID(file);
        elif choice == 'n' or choice == 'N':
            print("\nTry again.");
            excel_manipulation.choose_excel_file();
            
        else:
            print("\nThat isn't an option! Try again.");
            excel_manipulation.choose_excel_file();
            
        return excel_manipulation.load_excel_file(file);

class workflow():
    def working_directory():
           
        if os.path.exists('default_directory.txt') and os.stat('default_directory.txt').st_size != 0:
            default = open('default_directory.txt', 'r');
            os.chdir(str(default.read()));            
        else:
            print("\nThe set default directory doesn't exist. You may return to the main menu and set a new default directory,", 
                  "otherwise we'll use the current directory.");
            create_default = open('default_directory.txt', 'w+');
            create_default.write(str(os.getcwd()));
            create_default.close();
    
 
        print("\n------------\nBlast-off *\n------------\nThe current directory is: " + str(os.getcwd())+ "\nTo return to the main menu,",
        " enter(m). To view items in this directory, enter(v). To create a folder, enter(mf). To view the workflow, enter(wf).");
        choice = input("\nDo you want to work in this directory? Enter(y/n): ");
    
        if choice == 'y' or choice == 'Y':
            Ortholog_Report.report();
            excel_manipulation.choose_excel_file();  
            
        elif choice == 'n' or choice == 'N':
            files.change_directory();
            
        elif choice == 'm' or choice == 'M': # Return to the main menu.
            main()# Exit loop.
            
        elif choice == 'v' or choice == 'V': # View the contents of the current directory.
            files.view_directory();
           
        elif choice == 'mf':
            files.make_folder(); # Creates a new folder.
        
        elif choice == 'wf':
            files.open_text_file("research_workflow.txt"); # Opens the workflow textfile.
            
        else:
            print("That isn't an option! Try again."); # Input validation.
            workflow.working_directory();
        
    
    def webbrowser(link):
        global driver;
        
        try:
            gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
            binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
            driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe')
            #driver = webdriver.Firefox(executable_path=r"C:\\Program Files\\Mozilla Firefox\\Firefox.exe\\");
            driver.get(link);
        except:
                try:
                    driver = webdriver.Chrome(executable_path=r"chromedriver.exe");
                    driver.get(link);
                except (SessionNotCreatedException, NoSuchWindowException, WebDriverException) as error:
                    print("\nThe webpage was unable to be open. The link to the website is: " + link);
                    input("\nCopy and paste the link into your webbrowser and complete this step manually. Press enter once this step is completed");
                    pass;
        else:
            driver = webdriver.Safari();
            driver.get(link);
                
    def blast(cell1, cell2):
        workflow.webbrowser("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins&PROGRAM=blastp&BLAST_PROGRAMS=blastp&PAGE_TYPE=BlastSearch&BLAST_SPEC=blast2seq&DATABASE=n/a&QUERY=&SUBJECTS=");
        
        inputElement1 = driver.find_element_by_id("seq");
        inputElement2 = driver.find_element_by_id("subj");

        inputElement1.send_keys(cell1);
        inputElement2.send_keys(cell2);
    
    def batch(key, match_file):
        workflow.webbrowser("https://www.ncbi.nlm.nih.gov/sites/batchentrez");
        
        element1 = driver.find_element_by_name("file");
        element1.send_keys(key + "/" + match_file)
        element2 = Select(driver.find_element_by_name("db"));
        element2.select_by_value("protein");
    
    def align(key):
        alignment = input("\nOnce you've completed step 9, enter the name of the FASTA file: ");
        
        if os.path.exists(alignment):
            print("\nYou entered: " + alignment);
        elif os.path.exists(alignment) == False and os.path.exists(alignment + '.fasta'):
            alignment = alignment + '.fasta';
        else:
            print("\nThis file doesn't exist. Try again.");
            workflow.align(key);
            
        workflow.webbrowser("https://www.ebi.ac.uk/Tools/msa/clustalo");
        element3 = driver.find_element_by_name("upfile");
        element3.send_keys(key + "/" + alignment);
        element3.submit();
        
    def show_align(key):
        show_align = input("\nEnter the name of the multiple alignment file that you want to show align: ")
        
        if os.path.exists(show_align):
            print("\nYou entered: " + show_align);
        elif os.path.exists(show_align) == False and os.path.exists(show_align + '.txt'):
            show_align = show_align + '.txt';
        else:
            print("\nThis file doesn't exist. Try again.");
            workflow.show_align(key);
                   
        workflow.webbrowser("http://www.bioinformatics.nl/cgi-bin/emboss/showalign");
        element4 = driver.find_element_by_name("sequence.file");
        element4.send_keys(key + "/" + show_align);
            
def main(): # Main menu 
    choice = input("\n\nBlast-Off *\n------------\n1)Start\n2)Set default directory\n3)View Research Workflow\n4)Create a folder\n5)Exit\n");

    if choice == '1':
        workflow.working_directory(); # Starts the program.
    elif choice == '2':
        files.set_default_directory(); # Setting the default directory.
    elif choice == '3':
        files.open_text_file("research_workflow.txt"); # Opens the workflow text file.
    elif choice == '4':
        files.make_folder(); # Creates a new folder in the current directory.
    elif choice == '5':
        return 0; # Exits the program.
    else:
        print("That isn't an option! Try again."); # Input validation.
        main(); # Returns to the main menu.

if __name__=='__main__':
    main()
