# Relatório - Esteganografia

---

IFB - Instituto Federal de Brasília  
Processamento Digital de Imagens  
**Professor:** Raimundo Vasconcelos  
**Nome:** Henrique Tavares Aguiar  

---

## Codificar (```encode.py```)

O programa recebe seus argmentos por linha de comando da seguinte forma:

```bash
python3 encode.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png
```

Esses argumentos são validados no começo do programa através da função:

```python
def validate_args():
    try:
        image_in = sys.argv[1]
        text = sys.argv[2]
        bits_level = int(sys.argv[3])
        image_out = sys.argv[4]

        if not path.exists(path.join(path.curdir, image_in)):
            raise FileNotFoundError("First argument (image_in) invalid")

        if not path.exists(path.join(path.curdir, text)):
            raise FileNotFoundError("Second argument (text_in) invalid")

        if bits_level < 0 or bits_level > 3:
            raise ValueError("Third argument (bits_level) must be between 0 and 3")

    except IndexError:
        print(f"Expected 4 arguments, but got {len(sys.argv) - 1}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except ValueError as e:
        print(e)

    else:
        if image_in == image_out:
            print(
                "Warning: image_in and image_out are the same. image_in will be overwritten.",
                end="\n\n",
            )

        return image_in, text, bits_level, image_out
```

Nessa função é verificada se existe uma imagem de entrada, um arquivo de texto de entrada e se o argumento *bits_level* está entre os números: 0 \(R\), 1 (G), 2(B) e 3(RGB). Se qualquer um deles não for válido, a função retorna *None* e a execução termina.

```python
args = validate_args()
if args is None:
    exit(0)

image_in_arg, text_arg, bits_level, image_out = args
```

Os arquivos são lidos como demostrado abaixo (O módulo *Image* do pacote *PIL* foi usado para manipulação de imagem):

```python
with Image.open(image_in_arg) as image_in, open(text_arg) as text_file:
```

O texto é lido e colocado dentro de uma estrutura chamada *bytearray* do Python, que recebe uma *string* e uma codificação, e a transforma num *array* mutável de *bytes*. Cada elemento do *array* corresponde a um caractere da *string* original representado por um inteiro.

```python
text = text_file.read()
text_bytearray = bytearray(text, "utf-8")
```

Visto que cada elemento precisará ser convertido em uma representação de bits, e um byte corresponde à oito bits. Para armazenar essa nova estrutura ela teria oito vezes o tamanho do texto original, e levando em conta que o arquivo de texto pode não ser pequeno, essa estrutura consumiria muita memória. Por esse motivo, e para facilitar quando o argumento *bits_level* for 3, pois o texto teria que ser gravado nos três canais de cor em uma vez, foi usado um *generator iterator* do Python para iterar sobre o *bytearray*. O *generator iterator* tem tamnho constante, pois ele entrega apenas um elemento por vez, pode ser usado num *for-loop* ou manualmente através da função ```next()```, e quando ela chega ao último elemento a estrutura se esgota e não tem mais uso.

```python
text_bytearray_generator = (byte for byte in text_bytearray)
```

Antes de começar a gravar a mensagem dentro da imagem, foi feito uma verificação para assegurar que o texto cabe dentro da imagem.

```python
image_pixels = image_in.height * image_in.width
text_bits = len(text_bytearray) * 8

if (bits_level > 3 and text_bits > (image_pixels * 3)) or text_bits > image_pixels:
    print("Error: The text does not fit into the image")
    exit(0)
```

Para gravar a mensagem dentro da imagem, é necessário uma conversão do mesmo para bits (0 e 1). Então foi usado uma fila de bits, onde os bytes seriam convertidos apenas quando necessário, evitando gastar memória desnecessariamente. Isso foi feito com ajuda da seguinte função.

```python
def pop_with_generator(iterable, generator, default, handle_fallback):
    if len(iterable) == 0:
        value = next(generator, default)
        handle_fallback(iterable, value)

    return iterable.pop(0)
```

Assim que a fila se esgotar, a função *handle_fallback* se encarrega colocar os novos elementos, seu uso ficará mais claro no momento que é chamado.

A mensagem é gravada pixel a pixel da imagem, com a seguinte função.

```python
def transform_pixel(image, coordinate, bit_plane, bit):
    pixel = image.getpixel(coordinate)
    pixel_binary = f"{pixel[bit_plane]:08b}"
    pixel_binary_transformed = pixel_binary[:-1] + bit
    pixel_transformed = pixel[:bit_plane] + tuple([int(pixel_binary_transformed, base=2)]) + pixel[(bit_plane + 1) :]

    return pixel_transformed
```

Os pixels da imagem estão no formato RGB, a variável *bit_plane* é responsável por qual canal o bit será escrito. O valor inteiro do canal é convertido em bits, e tem o seu último bit trocado pelo bit da mensagem

De forma genral a mensagem é escrita da seguinte maneira:

```python
bit_buffer = []
for (x, y) in product(range(image_in.height), range(image_in.width)):
    if bits_level == 3:
        for i in range(3):
            bit = pop_with_generator(
                bit_buffer,
                text_bytearray_generator,
                0,
                lambda iterable, byte: iterable.extend(f"{byte:08b}"),
            )
            pixel_transformed = transform_pixel(image_in, (x, y), i, bit)
            image_in.putpixel((x, y), pixel_transformed)
    else:
        bit = pop_with_generator(
            bit_buffer,
            text_bytearray_generator,
            0,
            lambda iterable, byte: iterable.extend(f"{byte:08b}"),
        )
        pixel_transformed = transform_pixel(image_in, (x, y), bits_level, bit)
        image_in.putpixel((x, y), pixel_transformed)
```

No momento em que o texto acaba, o resto é preenchido com o bit 0. Depois da mensagem ser gravada a imagem transformada é salva com o nome especificado pelo argumento *image_out*.

```python
if not image_out.endswith(".png"):
    image_out += ".png"

image_in.save(path.join(path.curdir, image_out))
```

---

## Decodificar (```decode.py```)

Da mesma forma que o programa de codificar, os argumentos são passado por linha de comando:

```bash
python3 decode.py imagem_saida.png plano_bits texto_saida.txt
```

E os argumentos são validados também no começo do programa com a função:

```python
def validate_args():
    try:
        image_out = sys.argv[1]
        bits_level = int(sys.argv[2])
        text_out = sys.argv[3]

        if not path.exists(path.join(path.curdir, image_out)):
            raise FileNotFoundError("First argument (image_out) invalid")

        if bits_level < 0 or bits_level > 3:
            raise ValueError("Third argument (bits_level) must be between 0 and 3")

    except IndexError:
        print(f"Expected 3 arguments, but got {len(sys.argv) - 1}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")

    except ValueError as e:
        print(e)

    else:
        return image_out, bits_level, text_out
```

Nessa função é verificada se existe uma imagem de saída (saída da codificação), e se o argumento *bits_level* está entre 0 \(R\), 1 (G), 2 (B) e 3 (RGB). E se qualquer dos dois não for válido, a função retorna *None* e o programa termina.

```python
args = validate_args()
if args is None:
    exit(0)

image_out_arg, bits_level, text_out_arg = args
```

O arquivo de imagem é lido, enquanto o de texo, se existir é reescrito, e se não existir é criado. O arquivo de texto é aberto no modo *wb*, que significa escrita em modo binário.

```python
with Image.open(path.join(path.curdir, image_out_arg)) as image_out, open(text_out_arg, "wb") as text:
```

O funcionamento para decodificar a mensagem é bem similar ao processo de codificar. É usado uma fila de bits, que vai sendo preenchido conforme os bits são extraídos dos pixels. Assim que a fila atinge um tamanho de oito, os oito primeiros elementos ou bits são retirados da fila, e então transformados em um inteiro que representa um caractere. Esses valores vão sendo colocados dentro de um *bytearray*.

```python
text_bytearray = bytearray()
bit_buffer = []

for (x, y) in product(range(image_out.height), range(image_out.width)):
    pixel = image_out.getpixel((x, y))

    if bits_level == 3:
        for i in range(3):
            byte = pixel[i]
            byte_str = f"{byte:08b}"
            bit = byte_str[-1]
            bit_buffer.append(bit)
    else:
        byte = pixel[bits_level]
        byte_str = f"{byte:08b}"
        bit = byte_str[-1]
        bit_buffer.append(bit)

    if len(bit_buffer) >= 8:
        byte_str = "".join(bit_buffer[:8])
        byte = int(byte_str or "0", base=2)
        text_bytearray.append(byte)

        bit_buffer = bit_buffer[8:]
```

Agora, a mensagem inteira está contida no *bytearray text_bytearray*. Incluíndo o final que é irrelevante, porque essa parte contém apenas caracteres nulos ("\x00" é a representação do caractere nulo).

```python
stripped_text_bytearray = text_bytearray.strip(b"\x00")
```

Como o arquivo de texto foi aberto no modo binário, é possível de se escrever nele não com *strings* mas com bytes. Porém, é necessário uma última conversão para a estrutra *bytes* do Python, muito similar ao *bytearray*, porém essa é imutável.

```python
text_bytes = bytes(stripped_text_bytearray)
text.write(text_bytes)
```

---

## Testes realizados

Os testes foram realizados com essa imagem (225x225):
![baboon](https://i.imgur.com/YhUzD4v.png)

E com um texto Lorem Ipsum:

```text
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur fermentum egestas maximus. In eleifend, mi ac fermentum tempus, elit eros fermentum lectus, ut facilisis tortor massa in lorem. Duis vitae magna a tellus aliquam viverra. Nunc sit amet efficitur quam, non gravida purus. Aliquam nec iaculis turpis, a tristique sapien. Fusce interdum justo id eros venenatis vehicula. Aenean a tincidunt lacus. Etiam molestie neque ut quam consequat venenatis. Morbi vehicula egestas arcu, sed accumsan enim iaculis quis. Cras semper arcu ut tristique tincidunt. Cras dignissim urna sem, ac convallis nisl fermentum quis. Proin sed vehicula massa. Curabitur eleifend urna a dignissim venenatis.

Mauris lacinia sollicitudin quam eu aliquet. In semper pellentesque felis id porta. Nullam in dui ut purus lobortis consectetur. In semper dui maximus dolor bibendum pretium. Vestibulum a semper mauris. In varius eros ut placerat viverra. Phasellus eget tortor posuere, interdum nisl sed, finibus erat. Vivamus et interdum metus. Suspendisse viverra consectetur est vehicula luctus. Nulla mollis in est quis consequat. Praesent scelerisque metus fringilla orci suscipit, sed faucibus purus viverra. Praesent consequat vestibulum gravida.

Nulla facilisi. Donec sed porttitor lectus. Aliquam ullamcorper condimentum sem sed vehicula. In aliquet velit mollis, pulvinar metus vel, lobortis dolor. Ut fringilla nisi vitae rutrum elementum. Nunc suscipit ac ipsum in pulvinar. Suspendisse pellentesque metus vitae lacus tempor sagittis. Integer fringilla dignissim ligula, in dapibus neque pretium nec. Sed dictum iaculis eros ut pellentesque. Donec maximus dignissim lectus, molestie feugiat neque porta eget. Donec ac tempus mauris, eu vestibulum lectus. Donec iaculis, lectus eu semper pretium, elit odio semper ipsum, quis vestibulum lectus dui a erat. Quisque ac lectus sed nisl varius dignissim.

Morbi ultricies, tellus quis dictum vestibulum, nibh metus dictum justo, vel tristique nibh leo sit amet est. Aliquam pretium rutrum suscipit. Suspendisse dolor velit, ultricies id sollicitudin a, tincidunt nec metus. Maecenas malesuada dictum quam, elementum convallis justo egestas non. Duis rhoncus arcu sit amet nisl tempor vehicula. Nullam et lorem ac purus tincidunt aliquam in vel velit. Nulla placerat euismod nisi. Duis aliquam tempus nisl, ut volutpat ligula dignissim ullamcorper.

Etiam efficitur tristique volutpat. Mauris convallis orci a mi efficitur, sit amet tincidunt augue finibus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed ac posuere nibh. Phasellus vitae nunc sagittis, rutrum odio sed, accumsan nibh. Proin placerat ipsum nec purus pharetra, ut venenatis dui egestas. Nulla facilisi. Sed ut turpis ut erat tincidunt aliquam ac eu risus. Fusce fringilla, ligula non interdum laoreet, erat nulla finibus tortor, sit amet condimentum velit erat ut dui. Donec dapibus nisi orci, id luctus massa vehicula a. Vivamus enim justo, lacinia sed purus sit amet, iaculis dignissim odio. Integer quam ipsum, eleifend a posuere sit amet, dignissim vel ex. Proin scelerisque quam ut orci ornare, imperdiet auctor ipsum placerat. Proin lobortis maximus malesuada. Nulla id leo nec ipsum tempor lobortis aliquam quis nunc.
```

Para os quatro possíveis valores do argumento *bits_plane*. E em todos os testes, as fases de codificação e decodificação foram executadas com sucesso.

---

### Observações

Para fins didáticos, neste relatório relativo aos trechos de código, não foi utilizado os *type hints* do Python, que facilita o momento do desenvolvimento dos algoritmos, porque adiciona tipagem as variáveis. Mas não possui nenhum impacto na execução do programa.

Para a mensagem ser decodificada corretamente, o argumento *bits_level* precisa ser o mesmo tanto na fase de codificação quanto na fase de decodificação.
