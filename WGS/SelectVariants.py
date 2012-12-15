#!/software/bin/python

## T. Carstensen (tc9), M.S. Sandhu (ms23), D. Gurdasani (dg11)
## Wellcome Trust Sanger Institute, 2012

## http://www.broadinstitute.org/gatk/gatkdocs/org_broadinstitute_sting_gatk_walkers_variantutils_SelectVariants.html

import os

def main():

    '''this script finds concordance and discordance between VCF files generated by tc9 and mp15'''

    dbSNP = '/lustre/scratch107/projects/uganda/users/tc9/in_GATK/dbsnp_135.b37.vcf'

## Select all calls missed in my vcf, but present in HapMap (useful to take a look at why these variants weren't called by this dataset):
## java -Xmx2g -jar GenomeAnalysisTK.jar \
##   -R ref.fasta \
##   -T SelectVariants \
##   --variant hapmap.vcf \
##   --discordance myCalls.vcf
##   -o output.vcf \
##   -sn mySample

## --restrictAllelesTo BIALLELIC

    ##
    ## combinevariants
    ##
    walker = 'CombineVariants'
    fp_out = 'out_mp15/vqsr/vqsr_combinevariants.vcf'

    s = 'bsub \
    -o %s.out -e %s.err \
    -M4000000 -R\'select[mem>4000] rusage[mem=4000]\' \
    -J %s \
    java -Xmx4g \
    -jar /software/varinf/releases/GATK/GenomeAnalysisTK-1.4-15-gcd43f01/GenomeAnalysisTK.jar \
    -R /lustre/scratch111/resources/vrpipe/ref/Homo_sapiens/1000Genomes/human_g1k_v37.fasta \
    -T %s \
    ' %(walker, walker, walker, walker,)

    for chromosome in range(1,23)+['X','Y',]:
        s += ' --variant out_mp15/vqsr/%s.vqsr.filt.vcf ' %(chromosome)
    s += '-o %s' %(fp_out)
    
    if not os.path.isfile(fp_out):
        os.system(s)    

    ##
    ## discordance
    ##
    walker = 'SelectVariants'

##    fp_in1 = 'mp15_vqsr.vcf'

    for fp_in1, fp_in2, fp_out in [
        [
            'out_mp15/vqsr/vqsr_combinevariants.vcf',
            'out_GATK/join/ApplyRecalibration.recalibrated.filtered.vcf',
            'SelectVariants_discordance1.vcf',
            ],
        [
            'out_mp15/vqsr/vqsr_combinevariants.vcf',
            'out_GATK/join/ApplyRecalibration.recalibrated.filtered.vcf',
            'SelectVariants_discordance2.vcf',
            ],
        ]:
                                                              
        s = 'bsub \
        -o %s.out -e %s.err \
        -M4000000 -R\'select[mem>4000] rusage[mem=4000]\' \
        -J %s \
        java -Xmx4g \
        -jar /software/varinf/releases/GATK/GenomeAnalysisTK-1.4-15-gcd43f01/GenomeAnalysisTK.jar \
        -R /lustre/scratch111/resources/vrpipe/ref/Homo_sapiens/1000Genomes/human_g1k_v37.fasta \
        -T %s \
        --selectTypeToInclude SNP \
        --variant %s \
        --discordance %s \
        -o %s \
        ' %(walker, walker, walker, walker, fp_in1, fp_in2, fp_out,)
        if not os.path.isfile(fp_out):
            os.system(s)

    ##
    ## concordance
    ##
##    fp_in2 = 'mp15_vqsr.vcf'
    fp_in2 = 'out_mp15/vqsr/vqsr_combinevariants.vcf'
    fp_in1 = 'out_GATK/join/ApplyRecalibration.recalibrated.filtered.vcf'
    fp_out = 'SelectVariants_concordance.vcf'

    s = 'bsub \
    -o %s.out -e %s.err \
    -M4000000 -R\'select[mem>4000] rusage[mem=4000]\' \
    -J %s \
    java -Xmx4g \
    -jar /software/varinf/releases/GATK/GenomeAnalysisTK-1.4-15-gcd43f01/GenomeAnalysisTK.jar \
    -R /lustre/scratch111/resources/vrpipe/ref/Homo_sapiens/1000Genomes/human_g1k_v37.fasta \
    -T %s \
    --selectTypeToInclude SNP \
    --variant %s \
    --concordance %s \
    -o %s \
    ' %(walker, walker, walker, walker, fp_in1, fp_in2, fp_out,)
    if not os.path.isfile(fp_out):
        os.system(s)

    return

if __name__ == '__main__':
    main()