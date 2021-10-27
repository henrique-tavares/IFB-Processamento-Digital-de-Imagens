# Esteganografia

O objetivo deste trabalho é implementar um algoritmo de esteganografia em imagens digitais.

---

## *Encoding*

Para realizar a codificação de uma mensagem de texto para dentro de uma imagem, execute o programa ```encode.py``` da seguinte forma:

```shell
python3 encode.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png
```

## *Decoding*

Para realizar a decodificação de uma mensagem de texto para fora de uma imagem, execute o programa ```decode.py``` da seguinte forma:

```shell
python3 decode.py imagem_saida.png plano_bits texto_saida.txt
```

---

### Parâmetros

- ```imagem_entrada.png```: imagem no formato PNG em que será embutida a mensagem.

- ```imagem_saida.png```: imagem no formato PNG com mensagem embutida.

- ```texto_entrada.txt```: arquivo-texto contendo mensagem a ser oculta.

- ```texto_saida.txt```: arquivo-texto contendo mensagem recuperada.

- ```plano_bits```: três planos de bits menos significativos representados pelos valores 0 (R), 1 (G), 2 (B) ou 3 (RGB).
