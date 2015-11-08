Feature: Selcal Decoding
    In order to determine the Selcals being received
    As a user
    I want to decode received audio and extract any Selcal calls from it

    Scenario: Streaming audio
        Given I have a source of streaming audio at <Rate> kpbs
        When I use it as input
        Then I should get audio samples for processing every 100 mS

    Scenario: Audio files
        Given I have recorded audio in file <Name>
        When I use it as imput
        Then I should get audio samples for processing every 100 mS

    Scenario Outline: Tone detection
        Given I have a 100 mS audio sample containing tone <Designator>
        When I process it
        Then I should detect the tone <Frequency> +/- 0.15%
        Examples: Designators
        | Designator    | Frequency |
        | Alpha         | 312.6     |
        | Bravo         | 346.7     |
        | Charlie       | 384.6     |
        | Delta         | 426.6     |
        | Echo          | 473.2     |
        | Foxtrot       | 524.8     |
        | Golf          | 582.1     |
        | Hotel         | 645.7     |
        | Juliet        | 716.1     |
        | Kilo          | 794.3     |
        | Lima          | 881.0     |
        | Mike          | 977.2     |
        | Papa          | 1083.9    |
        | Quebec        | 1202.3    |
        | Romeo         | 1333.5    |
        | Sierra        | 1479.1    |

    Scenario Outline: Silence detection
        Given I have a 100 mS audio sample containing no tones
        When I process it
        Then I should detect no tones

    Scenario Outline: Pulse
        Given I have 15 100 mS audio samples
        And I detect silence in two consecutive samples
        And I detect the same two tones <A> and <B> in more than 7 and less than 13 consecutive samples
        Then I have detected a Pulse

    Scenario Outline: Selcal
        Given I have detected pulses <One> and <Two>
        And pulse <One> contains tones <A> and <B>
        And pulse <Two> contains tones <C> and <D>
        And tones <A>, <B>, <C>, <D> are all different
        Then the selcal <A><B>-<C><D> has been detected