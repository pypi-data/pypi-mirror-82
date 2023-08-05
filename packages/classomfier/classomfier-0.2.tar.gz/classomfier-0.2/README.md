# ClasSOMfier: A neural network for cluster analysis and detection of lattice defects


    Kohonen network that classifies atoms according to their environment.
    Unsupervised training using a 1-dimensional Self Organizing Map (SOM) in Fortran.
    
    Created by Javier F. Troncoso, October 2020.
        Contact: javierfdeztroncoso@gmail.com


  #   Installation:
    
      Option 1 (preferred):
        Use pip for Python3:
            $ pip install classomfier
            
      Option 2:
        Download the source code and build the package. Follow the instructions in file "install.sh". 
    
      Not tested on MacOs X and Windows. 
   
  #   Use:
        
        The network and its parameters can be initialized using the following command:
            >>from classomfier import ClasSOMfier
            >>nn=ClasSOMfier(6.43718,2,"dump1000.file")
        Only 3 parameters are necessary: characteristic length, number of clusters and input file.
        The number of epochs, the name of the output files and other parameters are optional. If the 
        number of atoms is large (>12000 approx), the option 'usenomatrix=True' has to be used. When
        this option is activated, the total running time increases considerably.
        The format of the input file is that provided by the dump command in LAMMPS:
            #compute         peratom all pe/atom
            #dump            dumpid2 all custom 1000 dump*.file id mass x y z c_peratom
        The first command calculates and stores the potential energy per atom.
            
        The network is trained using the following command:
            >>nn.execute()
        The final condigurations are written in ./data (default value) and can be easily read by Ovito. 
        These files includes xyz files for the atoms of each cluster and all atoms, and input files 
        with the set of input values for each cluster.
        
            
        The final configurations can be postprocessed to find subcategories inside a specific category:
            >>nn.postprocess_output()
        Afer this, the atoms of one of the clusters can be used to find subcategories:
            >>nn=ClasSOMfier(6.43718,2,"data/positions2.xyz",traininput="_trainset2.dat",useexisting=True)   
            >>nn.execute()
        Where "data/positions2.xyz" is the file containing the positions of the atoms in group 2 and 
        "_trainset2.dat" contains the description of the local environments of the atoms in that group. 
        As a result, these atoms will be classified and the final condigurations are written in 
        "./data/data" (default value).

        Input files in classomfier/test can be used as examples.
        
      
  #   Future Work:
        
        -Improve the performance for large systems.
        
      In the case of doubts or problems, all questions are welcome. Open to new collaborations.
