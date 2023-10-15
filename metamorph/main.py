from .quilt import QuiltLoaderTask


def main():
    luigi.build([QuiltLoaderTask()])
