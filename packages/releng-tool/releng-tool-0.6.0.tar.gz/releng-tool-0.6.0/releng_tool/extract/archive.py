# -*- coding: utf-8 -*-
# Copyright 2018-2020 releng-tool

from ..tool.tar import TAR
from ..util.io import execute
from ..util.io import interpret_stem_extension
from ..util.log import debug
from ..util.log import err
from ..util.log import warn
from zipfile import ZipFile
import os
import shutil
import tarfile

#: list of (most-likely) supported tar extraction extensions
TAR_SUPPORTED = (
    'tar',
    'tb2',
    'tbz2',
    'tgz',
)

def extract(opts):
    """
    support extraction of an archive into a build directory

    With provided extraction options (``RelengExtractOptions``), the extraction
    stage will be processed. The archive's extension will be used in attempt to
    finding a matching tool/implementation which can be used to extract the
    contents of the file. In the event that the method of extraction cannot be
    determined, it will be assumed that the file is in fact not extractable.
    Files which are not extracted are just copied into the build directly (e.g.
    single resource files).

    Args:
        opts: the extraction options

    Returns:
        ``True`` if the extraction stage is completed; ``False`` otherwise
    """

    assert opts
    cache_file = opts.cache_file
    strip_count = opts.strip_count
    work_dir = opts.work_dir

    cache_basename = os.path.basename(cache_file)
    __, cache_ext = interpret_stem_extension(cache_basename)

    is_extractable = False
    if cache_ext:
        cache_ext = cache_ext.lower()
        # if the user defines a tool override for this extension type, use
        # whatever the user wants to use (passing the file and directory to
        # extract to)
        if opts._extract_override and cache_ext in opts._extract_override:
            is_extractable = True

            tool_cmd = opts._extract_override[cache_ext].format(
                file=cache_file, dir=work_dir)

            if not execute(tool_cmd.split(), cwd=work_dir, critical=False):
                err('unable to extract with tool override')
                err(' (command: {})'.format(tool_cmd))
                return None

        # attempt to extract the (compressed) tar archive with the host's
        # tar tool; if it does not exist, we'll fallback to using python's
        # internal implementation (tarfile)
        elif cache_ext.startswith(TAR_SUPPORTED):
            is_extractable = True

            has_extracted = False
            if TAR.exists():
                if TAR.execute([
                        '--extract',
                        '--file=' + cache_file,
                        '--force-local',
                        '--strip-components={}'.format(strip_count),
                        '--verbose'],
                        cwd=work_dir):
                    has_extracted = True
                else:
                    warn('unable to extract archive with host tar; '
                        'will use fallback')

            if not has_extracted:
                try:
                    def tar_extract(members, strip_count):
                        for member in members:
                            # strip members from package defined count
                            if strip_count > 0:
                                np = os.path.normpath(member.name)
                                parts = np.split(os.path.sep, strip_count)
                                if len(parts) <= strip_count:
                                    continue
                                member.name = parts[-1]

                            # notify the user of the target member to extract
                            print(member.name)
                            yield member

                    with tarfile.open(cache_file, 'r') as tar:
                        tar.extractall(path=work_dir,
                            members=tar_extract(tar, strip_count))
                except Exception as e:
                    err('unable to extract tar file')
                    err('    {}'.format(e))
                    err(' (file: {})'.format(cache_file))
                    err(' (target: {})'.format(work_dir))
                    return False

        # extract a zip-extension cache file using python's internal
        # implementation (zipfile)
        elif cache_ext == 'zip':
            is_extractable = True

            try:
                with ZipFile(cache_file, 'r') as zip_:
                    for member in zip_.namelist():
                        # strip members from package defined count
                        member_s = member
                        if strip_count > 0:
                            np = os.path.normpath(member_s)
                            parts = np.split(os.path.sep, strip_count)
                            if len(parts) <= strip_count:
                                continue
                            member_s = parts[-1]
                        dest = os.path.join(work_dir, member_s)

                        # notify the user of the target member to extract
                        print(member)
                        if not os.path.basename(member):
                            os.mkdir(dest)
                        else:
                            with zip_.open(member) as src, open(dest, 'wb') as f:
                                shutil.copyfileobj(src, f)

            except Exception as e:
                err('unable to extract zip file')
                err('    {}'.format(e))
                err(' (file: {})'.format(cache_file))
                err(' (target: {})'.format(work_dir))
                return False

    if not is_extractable:
        debug('file not considered extractable: ' + cache_file)
        try:
            shutil.copy2(cache_file, work_dir)
        except IOError as e:
            err('unable to copy over cache file')
            err('    {}'.format(e))
            err(' (file: {})'.format(cache_file))
            err(' (target: {})'.format(work_dir))
            return False

    return True
