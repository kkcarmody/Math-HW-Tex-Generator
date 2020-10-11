from pathlib import Path
import getpass


def print_dirs(current_dirs):
    ''' Prints each folder in the dict current_dirs '''
    print('\nCurrent course directories:')
    for folder in current_dirs:
        print(' ' + folder)


def get_dir():
    ''' Gets user input and returns course name and path to target directory for project; creates dir if needed

    :return: str, Path
    '''
    user = getpass.getuser()
    user_path = Path(''.join(['C:Users/', user, '/OneDrive/Coursework/']))  # set to your dir for coursework
    current_dirs = {str(folder).split('\\')[-1]: folder for folder in user_path.iterdir() if folder.is_dir()}

    valid_choice = 0
    print_dirs(current_dirs)
    course = input("\nInput course num this assignment is for, [e.g., CIT 591].")

    while not valid_choice:
        matches = [course in folder for folder in current_dirs]
        valid_choice = sum(matches)
        if valid_choice > 1:
            valid_choice = 0
            print('Input matches more than one directory.')
        elif valid_choice:
            match = {x : y for x, y in zip(matches, current_dirs)}.get(1)
            target_path = user_path / match
            continue
        else:
            if input('Course directory not found. Create directory? [y/n]') == 'y':
                course_name = input("Course name [e.g., 'Measure Theory']")
                dir_name = ' - '.join([course, course_name])
                target_path = user_path / dir_name
                target_path.mkdir(parents=False)
                valid_choice = 1
                return course, target_path
            else:
                print_dirs(current_dirs)
                course = input("\nInput course num this assignment is for, [e.g., CIT 591].")

    return course, target_path


class LatexProject:
    def __init__(self):
        self.course, self.parent_path = get_dir()
        self.get_attributes()

    def get_attributes(self):
        self.attributes = {}
        self.attributes['title'] = input(" Title of your project [e.g., 'HW 6'] = ")
        self.attributes['doc_title'] = ''.join([self.course, ' : ', self.attributes.get('title')])
        self.attributes['author'] = input(' Author = ')
        self.attributes['date'] = input(' Due date = ')
        self.attributes['problems'] = list(input(" Input HW problems [e.g., '2.1, 2.25, 2.36, 3.1']").split(', '))

    def write_file(self, name, lines):
        file_out = self.path / name
        for line in lines:
            file_out.open('a').write(''.join([line, '\n']))

    def gen_main(self):
        main_template_path = Path.cwd() / 'template_main.tex'
        main_template = [line.rstrip() for line in main_template_path.open('r')]
        title_index = main_template.index('\\title{insert_title}')
        target_indices = {title_index : 'doc_title',
                          title_index + 1 : 'author',
                          title_index + 2 : 'date'}
        for i in target_indices.keys():
            attribute = target_indices.get(i)
            main_template[i] = ''.join(['\\', attribute, '{', self.attributes[attribute], '}'])

        prob_index = main_template.index('insert_problems')
        main_template[prob_index] = ''
        for prob in reversed(self.attributes.get('problems')):
            main_template.insert(prob_index, ''.join(['\\input{', prob, '}']))

        self.write_file('main.tex', main_template)
        print('\n Successfully made file main.tex!')

    def gen_preamble(self):
        preamble_path = Path.cwd() / 'preamble.sty'
        preamble_template = [line.rstrip() for line in preamble_path.open('r')]
        self.write_file('preamble.sty', preamble_template)
        print(' Successfully made file preamble.sty!')

    def gen_problems(self):
        problems = self.attributes.get('problems')
        sections = [prob.split('.')[0] for prob in problems]
        sections = {sections.index(prob) : prob for prob in sections}

        for prob in problems:
            prob_file = [''.join(['\\begin{problem}[', prob, ']\\label{pr', prob, '}']), '',
                         '\\end{problem}', '',
                         '\\noindent\\textit{Solution:} \\\\', '', '',
                         '\\vspace{10mm}']
            prob_index = problems.index(prob)
            if prob_index in sections:
                prob_file.insert(0, ''.join(['\\section*{', sections.get(prob_index), ' }']))

            file_name = ''.join([prob, '.tex'])
            self.write_file(file_name, prob_file)
            print(' Successfully made file ' + file_name + '!')

    def make_dir(self):
        self.path = self.parent_path / self.attributes.get('title')
        self.path.mkdir()
        print('-'*80 + '\n Made folder at ' + str(self.path))

        self.gen_main()
        self.gen_preamble()
        self.gen_problems()


if __name__ == '__main__':
    project = LatexProject()
    project.make_dir()
    print('-'*80 + 'All done!')