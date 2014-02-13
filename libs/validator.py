import sys

if sys.version_info[0]<3:
    sys.stderr.write("error: you need python 3.0 or later to run GIM.\n")
    sys.exit(1)

def validate_args(sys_args, args):
    from . import blast


    if len(sys_args) ==1:
      parser.print_usage()
      sys.stderr.write(sys.argv[0] + " Call with '-h' to get usage information.\n" )
      sys.exit(1)

    blasts = []
    for f in [args.blast1, args.blast2]:
        try:
            fh = open(f)
        except:
            sys.stderr.write(sys_args[0] + ": error: file {0} does not exists\n".format(f))  
            sys.exit(1)

        try:
            b = blast.read(fh, args.evalue)
            blasts.append(b)
            fh.close()
        except:
            sys.stderr.write(sys_args[0] + ": error: file {0} not in -m8/9 BLAST format\n".format(f))             
            sys.exit(1)
    return blasts
