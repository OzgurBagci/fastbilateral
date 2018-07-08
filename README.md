This code highly inspired by:

	[1] https://gist.github.com/ginrou/02e945562607fad170a1#file-fastbilateral-hpp
	[2] https://gist.github.com/jackdoerner/b81ad881c4064470d3c0#file-bilateral_approximation-py
	[3] https://github.com/KirillLykov/cvision-algorithms/blob/master/src/fastBilateralFilter.m
	[4] http://people.csail.mit.edu/jiawen/software/bilateralFilter.m
	
How to Use:
	Information of functions provided in script functions. If you want to use a standartized version use:
		python3 runner.py
	and type filenames with locations. Type '!-end-!' to end giving inputs. At least 2 images are needed.
	This method adds Random Gaussian Noise to images and processed with Bilateral Filter Implementations.
	
	To reduce resolution of images before processing:
		python3 lowerres.py
	Inputs work exactly as runner.py.
	
How It Works:
	Refer to The Report, The Fast Approximation. For more information a paper is provided in The Report.
		
Notes:
	There is no strict memory managment in 'runner.py' as it is just a testing script.
	The picked configurations are explaned in The Report.
	For more information contact one of the emails provided in 'fastbilateralapprox.py'.
