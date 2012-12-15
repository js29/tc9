#!/software/bin/python

## T. Carstensen (tc9), M.S. Sandhu (ms23), D. Gurdasani (dg11)
## Wellcome Trust Sanger Institute, 2012

import optparse, os

class main:

    def main(self,):

        opts = self.parse_args()
        threshold_min_novelTiTv = 2.1

        ## avoid raising an error if file is empty
        if os.path.getsize(opts.fp_in) == 0:
            return

        fd = open(opts.fp_in,'r')
        lines = fd.readlines()
        fd.close()
        l_headers = None
        for i_line in range(len(lines)):
            line = lines[i_line]
            ## comment
            if line[0] == '#':
                continue
            ## values
            l = line.strip().split(',')
            ## header
            if l_headers == None:
                l_headers = l
                continue
            ## body

            ## break the loop, once the TS is below a 2.1 threshold
            ## http://www.broadinstitute.org/gsa/wiki/index.php/Variant_quality_score_recalibration
            ## "I took called variants until I found 99% of my known variable sites"
            y2 = novelTiTv = float(l[l_headers.index('novelTiTv')])
            if novelTiTv < threshold_min_novelTiTv:
                x2 = targetTruthSensitivity = float(l[l_headers.index('targetTruthSensitivity')])
                ## Ti/Tv is already below 2.1 at lowest TS (i.e. 90)
                if i_line == 3 and targetTruthSensitivity == 90.:
                    TS = 90.
                else:
                    y1 = novelTiTv_prev = float(lines[i_line-1].strip().split(',')[l_headers.index('novelTiTv')])
                    x1 = targetTruthSensitivity_prev = float(lines[i_line-1].strip().split(',')[l_headers.index('targetTruthSensitivity')])
                    slope = (y2-y1)/(x2-x1)
                    intercept = y1-slope*x1
                    TS = (2.1-intercept)/slope
                break

        fd = open(opts.fp_out,'w')
        fd.write('%s' %(TS))
        fd.close()

        print 'TS was determined to be', TS

        return


    def parse_args(self,):

        instance_OptionParser = optparse.OptionParser()

        instance_OptionParser.add_option(
            '-i', '--input',
            help='File path of .tranches file generated by GATK VariantRecalibrator (e.g. out_GATK/VariantRecalibrator.tranches)',
            dest='fp_in',
            )
        instance_OptionParser.add_option(
            '-o', '--output',
            help='File path of file to which the TS value is written (e.g. out_Tommy/TS.22.txt)',
            dest='fp_out',
            )

        (opts, args) = instance_OptionParser.parse_args()

        l_mandatories = ['fp_in','fp_out',]
        bool_missing = False
        for m in l_mandatories:
            if not opts.__dict__[m]:
                print "The mandatory option %s is missing\n" %(m)
                bool_missing = True
        if bool_missing == True:
            instance_OptionParser.print_help()
            exit(-1)

        return opts

if __name__ == '__main__':
    instance_main = main()
    instance_main.main()