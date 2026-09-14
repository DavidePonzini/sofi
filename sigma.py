import statistics
import dav_tools


if __name__ == '__main__':
    dav_tools.argument_parser.add_argument(
        'filename',
        help='File containing one float per line'
    )

    args = dav_tools.argument_parser.args

    with open(args.filename) as f:
        values = [float(line.strip()) for line in f if line.strip()]

    average = statistics.mean(values)
    sigma = statistics.stdev(values)
    error = sigma / (len(values) ** 0.5)

    dav_tools.messages.info(f'Average: {average}')
    dav_tools.messages.info(f'Sigma:   {sigma}')
    dav_tools.messages.info(f'Error:   {error}')
