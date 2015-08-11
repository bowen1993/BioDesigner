import os
import django
import sys
import traceback
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from system.models import compound, gene, reaction, reaction_compound

def saveCompoundDataToDB(compound_file):
    current_info_type = ''
    compound_info = dict()
    for line in compound_file.readlines():
        if line.endswith('\n'):
            line = line[:-1]
        infos = line.split(' ')
        if not line.startswith(' ') and not line.startswith('/'):
            current_info_type = infos[0]
            infos = infos[1:]
        for info_item in infos:
            if info_item.endswith('\n'):
                info_item = info_item[:-1]
            if info_item == 'Compound' and current_info_type == 'ENTRY':
                continue
            try:
                compound_info[current_info_type] += info_item
            except:
                compound_info[current_info_type] = info_item
    #gene nick names
    try:
        names = compound_info['NAME'].split(';')
        compound_info['NAME'] = names[0]
        compound_info['NICKNAME'] = ''
        for i in range(1, len(names)):
            compound_info['NICKNAME'] += names[i] + '_'
        new_compound = compound(compound_id=compound_info['ENTRY'])
        new_compound.name = compound_info['NAME']
        new_compound.nicknames = compound_info['NICKNAME']
        new_compound.formula = compound_info['FORMULA']
        new_compound.exact_mass = compound_info['EXACT_MASS']
        new_compound.mol_mass = compound_info['MOL_WEIGHT']
        try:
            new_compound.save()
        except:
            traceback.print_exc()
            print '%s can not be saved' % compound_info['NAME']
    except:
        pass

def saveGeneDataToDB(gene_file):
    current_info_type = ''
    compound_info = dict()
    for line in gene_file.readlines():
        if line.endswith('\n'):
            line = line[:-1]
        if line.startswith('/'):
            continue
        infos = line.split(' ')
        if not line.startswith(' ') and not line.startswith('/'):
            current_info_type = infos[0]
            infos = infos[1:]
            if current_info_type == 'ENTRY':
                for info_item in infos:
                    if info_item != '':
                        compound_info['ENTRY'] = info_item
                        break
            if current_info_type == 'NTSEQ':
                for info_item in infos:
                    if info_item != '':
                        compound_info['NTSEQLEN'] = int(info_item)
                        break
            if current_info_type == 'ORGANISM':
                orStr = line.replace('ORGANISM    ', '')
                orList = orStr.split('  ')
                compound_info['ORGANISM_SHORT'] = orList[0]
                compound_info['ORGANISM'] = orList[1]
        for info_item in infos:
            if info_item.endswith('\n'):
                info_item = info_item[:-1]
            if current_info_type == 'ENTRY' or current_info_type == 'ORGANISM':
                continue
            if line.startswith('NTSEQ'):
                continue
            try:
                compound_info[current_info_type] += info_item
            except:
                compound_info[current_info_type] = info_item           
    try:
        names = compound_info['NAME'].split(';')
        compound_info['NAME'] = names[0]
        compound_info['NICKNAME'] = ''
        for i in range(1, len(names)):
            compound_info['NICKNAME'] += names[i] + '_'
        new_gene = gene(gene_id=compound_info['ENTRY'])
        new_gene.name = compound_info['NAME']
        new_gene.nicknames = compound_info['NICKNAME']
        new_gene.definition = compound_info['DEFINITION']
        new_gene.organism_short = compound_info['ORGANISM_SHORT']
        new_gene.organism = compound_info['ORGANISM']
        new_gene.position = compound_info['POSITION']
        new_gene.ntseq_length = compound_info['NTSEQLEN']
        new_gene.ntseq = compound_info['NTSEQ']
        try:
            new_gene.save()
        except:
            traceback.print_exc()
            print '%s can not be saved' % compound_info['NAME']
    except:
        traceback.print_exc()
    
def saveReactionDataToDB(reaction_file):
    current_info_type = ''
    reaction_info = dict()
    for line in reaction_file.readlines():
        if line.startswith('//'):
            continue
        if line.endswith('\n'):
            line = line[:-1]
        infos = line.split(' ')
        if not line.startswith(' ') and not line.startswith('/'):
            current_info_type = infos[0]
            infos = infos[1:]
        for info_item in infos:
            if info_item.endswith('\n'):
                info_item = info_item[:-1]
            if info_item == 'Reaction' and current_info_type == 'ENTRY':
                continue
            if current_info_type == 'EQUATION' and info_item != '':
                info_item += '_'
            try:
                reaction_info[current_info_type] += info_item
            except:
                reaction_info[current_info_type] = info_item
    try:
        new_reaction = reaction(reaction_id=reaction_info['ENTRY'])
        new_reaction.name = reaction_info['NAME']
        new_reaction.definition = reaction_info['DEFINITION']
        new_reaction.equation = reaction_info['EQUATION']
        new_reaction.save()
    except:
        pass

def getReactantList(equaStr):
    reactantStr = equaStr.split('<=>')[0]
    if reactantStr.endswith('_'):
        reactantStr = reactantStr[:-1]
    c_list = reactantStr.split('_')
    result_list = list()
    amount = 1
    for c in c_list:
        if c == '+':
            continue
        if c.isdigit():
            amount = int(c)
        try:
            compound_obj = compound.objects.get(compound_id=c)
            c_info = {
                'id': c,
                'amount' : amount,
            }
            result_list.append(c_info)
            amount = 1
        except:
            pass
    return result_list

def getResultantList(equaStr):
    reactantStr = equaStr.split('<=>')[1]
    if reactantStr.endswith('_'):
        reactantStr = reactantStr[:-1]
    c_list = reactantStr.split('_')
    result_list = list()
    amount = 1
    for c in c_list:
        if c == '+':
            continue
        if c.isdigit():
            amount = int(c)
        try:
            compound_obj = compound.objects.get(compound_id=c)
            c_info = {
                'id': c,
                'amount' : amount,
            }
            result_list.append(c_info)
            amount = 1
        except:
            pass
    return result_list

def anaRectEqua(ract):
    print 'analyzing %s' % ract.reaction_id
    ract_id = ract.reaction_id
    equaStr = ract.equation
    if equaStr.startswith('_'):
        equaStr = equaStr[1:]
    if equaStr.endswith('_'):
        equaStr = equaStr[:-1]
    reactant_list = getReactantList(equaStr)
    resultant_list = getResultantList(equaStr)
    for reactant in reactant_list:
        new_rc = reaction_compound(reaction_id = ract_id)
        new_rc.compound_id = reactant['id']
        new_rc.isReactant = True
        new_rc.amount = reactant['amount']
        new_rc.save()
    for resultant in resultant_list:
        new_rc = reaction_compound(reaction_id = ract_id)
        new_rc.compound_id = resultant['id']
        new_rc.isResultant = True
        new_rc.amount = resultant['amount']
        new_rc.save()


def anaReactionEquations():
    all_reactions = reaction.objects.all()
    for ract in all_reactions:
        anaRectEqua(ract)

def anaCompoundData(basepath):
    for parentDir, dirnames, filenames in os.walk(basepath):
        for filename in filenames:
            if filename.endswith('_Compound'):
                fullFilename = (parentDir if parentDir.endswith('/') else parentDir + '/') + filename
                compound_file = open(fullFilename, 'r')
                saveCompoundDataToDB(compound_file)

def anaGeneData(basepath):
    for parentDir, dirnames, filenames in os.walk(basepath):
        for filename in filenames:
            if filename.endswith('_Gene'):
                fullFilename = (parentDir if parentDir.endswith('/') else parentDir + '/') + filename
                gene_file = open(fullFilename, 'r')
                saveGeneDataToDB(gene_file)

def anaReactionData(basepath):
    for parentDir, dirnames, filenames in os.walk(basepath):
        for filename in filenames:
            if filename.endswith('_Reaction'):
                fullFilename = (parentDir if parentDir.endswith('/') else parentDir + '/') + filename
                reaction_file = open(fullFilename, 'r')
                saveReactionDataToDB(reaction_file)


if __name__ == '__main__':
    django.setup()
    anaReactionEquations()