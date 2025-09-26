#!/bin/bash


INPUT_SEQUENCE="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED"
SKIP_TRAINING="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--sequence)
            INPUT_SEQUENCE="$2"
            shift 2
            ;;
        --skip-training)
            SKIP_TRAINING="true"
            shift
            ;;
        *)
            echo "Неизвестный параметр: $1"
            exit 1
            ;;
    esac
done

echo "Запуск пайплайна с параметрами:"
echo "Цепочка: $INPUT_SEQUENCE"
echo "Пропустить обучение: $SKIP_TRAINING"

mkdir -p data output

export INPUT_SEQUENCE
export SKIP_TRAINING
docker compose down 2>/dev/null
docker compose up --build