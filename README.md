# FICO T1

FICO is a multidisciplinary interest group in Computational Finance and Systematic
Investments are operating.

## Project

O projeto teve origem no âmbito do curso de Aprendizado de Máquina em Finanças, no Programa de Pós-Graduação em Pesquisa Operacional, no Instituto Tecnológico de Aeronáutica (ITA), em São José dos Campos, SP, Brasil. O projeto é uma **Implementação do Modelo de 5 Fatores no Mercado Brasileiro**, com a aplicação de testes estatísticos para validar a significância de cada um dos fatores na explicação do retorno médio das ações que compõem o índice B3. Este projeto está disponível no repositório do [GitHub](https://github.com/fico-ita/po_245_2023_T1).


## Usage

### Installation

```bash
# Activate the virtual environment
cd project_folder
poetry shell

# Add the project packages
poetry add git+https://github.com/fico-ita/po_245_2023_T1.git

# Install the project packages
poetry install
```

### Requirements

Python 3.11 or higher is required. The project requires the following packages:

- `pandas`
- `numpy`
- `scikit-learn`


## Documentation
To make proper usage of the MKDocs, run these commands:
```bash
poetry shell
mkdocs serve
```
The documentation is available on [GitHub](
    http://127.0.0.1:8000/
    )

## License

[Apache License 2.0](LICENSE)

## Citation

Since this project is research-based, citing it in your work is essential.
To cite this project, use the following reference:

### BibTeX

```bibtex
@misc{Zanchitta2023finance,
    author = {Zanchitta,F. G.},
    title = {Implementação do Modelo Fama e French 5 fatores aplicado ao Mercado de ações brasileiro},
    year = {2023},
    DOI = {10.5281/IEEE.0000000},
    publisher = {IEEE},
    url = {https://doi.org/10.5281/IEEE.0000000}
}
```

### APA

```text
Zanchitta,F. G.(2023), Implementação do Modelo Fama e French 5 fatores aplicado ao Mercado de ações brasileiro.
```
