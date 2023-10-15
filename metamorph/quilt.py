from luigi import Task, LocalTarget
from luigi.parameter import Parameter, BoolParameter

import requests
import json
import urllib.parse

from .model.quilt import LoaderVersions


def maven_url(repository, specifier, extension):
    parts = specifier.split(":", 3)
    maven_ver_url = (
        repository + parts[0].replace(".", "/") + "/" + parts[1] + "/" + parts[2] + "/"
    )
    maven_url = maven_ver_url + parts[1] + "-" + parts[2] + extension
    return maven_url


class QuiltFetchJarInfoTask(Task):
    maven = Parameter()

    def run(self):
        # TODO: implement
        pass

    def output(self):
        return LocalTarget(is_tmp=True)


class QuiltFetchLoaderInstallerTask(Task):
    maven = Parameter()

    def run(self):
        url = maven_url(
            "https://maven.quiltmc.org/repository/release/", self.maven, "json"
        )
        # TODO: implement

    def output(self):
        return LocalTarget(is_tmp=True)


class QuiltGenLoaderTask(Task):
    maven = Parameter()
    version = Parameter()

    def requires(self):
        return {
            "installer": QuiltFetchLoaderInstallerTask(self.maven),
            "artifact": QuiltFetchJarInfoTask(self.maven),
        }

    def run(self):
        # TODO: implement
        pass

    def output(self):
        return LocalTarget(is_tmp=True)


class QuiltFetchComponentVersionsTask(Task):
    component = Parameter()

    def run(self):
        url = f"https://meta.quiltmc.org/v3/versions/{self.component}"
        with self.output().open("w") as f:
            r = requests.get(url)
            r.raise_for_status()
            versions = LoaderVersions.parse_obj(r.json())
            f.write(versions.json())

    def output(self):
        return LocalTarget(path=f"/tmp/quilt/{self.component}-versions.json")


class QuiltLoaderTask(Task):
    def requires(self):
        return QuiltFetchComponentVersionsTask(component="loader")

    def run(self):
        with self.input().open("r") as f:
            versions = LoaderVersions.parse_raw(f.read())
            # TODO: ugly
            for v in iter(versions.__root__):
                yield QuiltGenLoaderTask(maven=v.maven, version=v.version)
