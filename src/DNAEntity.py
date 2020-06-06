import pygame

from src.Interfaces.GeneCode import GeneCode
from src.Interfaces.RenderObject import RenderObject


class DNAEntity(RenderObject, GeneCode):
    def __init__(self, parent, dna_type: str, r) -> None:
        RenderObject.__init__(self, parent=parent)
        GeneCode.__init__(self)
        self.__image = pygame.image.load("{0}/dna_{1}.png".format(self._res_dir, dna_type)).convert_alpha()
        self.__dna_type = dna_type
        self.resource = r
        if dna_type == "worker":
            self.dna_code = "1"
        elif dna_type == "warrior":
            self.dna_code = "2"
        else:
            self.dna_code = "3"
        self._rect = self.__image.get_rect()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.__image, self._rect)
