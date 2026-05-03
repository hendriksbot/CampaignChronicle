"""this module contains the path utils that resolves path differences between
python app and the final distribution which happen due to packaging"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Iterable
import sys
import importlib

PathLike = Union[str, Path]


def _is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def _dist_base() -> Path:
    return Path(sys.executable).parent


def _package_root_from_pkgname(pkg: str) -> Path:
    m = importlib.import_module(pkg)
    return Path(m.__file__).resolve().parent


@dataclass
class _Entry:
    name: str
    dev_rel: Path
    frozen_candidates: tuple[Path, ...]
    create: bool = False

    def candidates_for(self, base_dev: Path, base_frozen: Path) -> list[Path]:
        if _is_frozen():
            return [base_frozen / c for c in self.frozen_candidates]
        return [base_dev / self.dev_rel]


@dataclass
class ResourceLocator:
    """
    A small registry that resolves resource paths in both dev and frozen builds.
    """

    dev_pkg_root: Path
    frozen_base: Path | None = None
    contents_dir: str = "_internal"
    _entries: dict[str, _Entry] = field(default_factory=dict)

    @classmethod
    def from_package(
        cls, package_name: str, contents_dir: str = "_internal"
    ) -> "ResourceLocator":
        dev_pkg_root = _package_root_from_pkgname(package_name)
        frozen_base = _dist_base() if _is_frozen() else None
        return cls(
            dev_pkg_root=dev_pkg_root,
            frozen_base=frozen_base,
            contents_dir=contents_dir,
        )

    def register(
        self,
        name: str,
        *,
        dev_rel: PathLike,
        frozen_rel_candidates: Iterable[PathLike] | None = None,
        create: bool = False,
    ):
        dev_rel = Path(dev_rel)
        candidates = tuple(
            Path(p) for p in (frozen_rel_candidates or (dev_rel,))
        )
        self._entries[name] = _Entry(
            name=name,
            dev_rel=dev_rel,
            frozen_candidates=candidates,
            create=create,
        )

    def path(self, name: str) -> Path:
        """
        resolve the path for 'name'. In frozen mode, returns the first
        existing candidate.
        """

        if name not in self._entries:
            raise KeyError(f"Resource '{name}' is not registered")

        entry = self._entries[name]
        base_dev = self.dev_pkg_root
        base_frozen = self.frozen_base or _dist_base()

        for p in entry.candidates_for(base_dev, base_frozen):
            if p.exists():
                return p

    def join(self, name: str, *parts: PathLike) -> Path:
        """convenience to append additional subpaths to a registered resource"""
        return self.path(name).joinpath(*map(Path, parts))
